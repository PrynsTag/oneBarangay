/**
 * @popperjs/core v2.9.3 - MIT License
 */

'use strict'

Object.defineProperty(exports, '__esModule', { value: true })

function getWindow (node) {
  if (node == null) {
    return window
  }

  if (node.toString() !== '[object Window]') {
    const ownerDocument = node.ownerDocument
    return ownerDocument ? ownerDocument.defaultView || window : window
  }

  return node
}

function isElement (node) {
  const OwnElement = getWindow(node).Element
  return node instanceof OwnElement || node instanceof Element
}

function isHTMLElement (node) {
  const OwnElement = getWindow(node).HTMLElement
  return node instanceof OwnElement || node instanceof HTMLElement
}

function isShadowRoot (node) {
  // IE 11 has no ShadowRoot
  if (typeof ShadowRoot === 'undefined') {
    return false
  }

  const OwnElement = getWindow(node).ShadowRoot
  return node instanceof OwnElement || node instanceof ShadowRoot
}

const round = Math.round
function getBoundingClientRect (element, includeScale) {
  if (includeScale === void 0) {
    includeScale = false
  }

  const rect = element.getBoundingClientRect()
  let scaleX = 1
  let scaleY = 1

  if (isHTMLElement(element) && includeScale) {
    // Fallback to 1 in case both values are `0`
    scaleX = rect.width / element.offsetWidth || 1
    scaleY = rect.height / element.offsetHeight || 1
  }

  return {
    width: round(rect.width / scaleX),
    height: round(rect.height / scaleY),
    top: round(rect.top / scaleY),
    right: round(rect.right / scaleX),
    bottom: round(rect.bottom / scaleY),
    left: round(rect.left / scaleX),
    x: round(rect.left / scaleX),
    y: round(rect.top / scaleY)
  }
}

function getWindowScroll (node) {
  const win = getWindow(node)
  const scrollLeft = win.pageXOffset
  const scrollTop = win.pageYOffset
  return {
    scrollLeft: scrollLeft,
    scrollTop: scrollTop
  }
}

function getHTMLElementScroll (element) {
  return {
    scrollLeft: element.scrollLeft,
    scrollTop: element.scrollTop
  }
}

function getNodeScroll (node) {
  if (node === getWindow(node) || !isHTMLElement(node)) {
    return getWindowScroll(node)
  } else {
    return getHTMLElementScroll(node)
  }
}

function getNodeName (element) {
  return element ? (element.nodeName || '').toLowerCase() : null
}

function getDocumentElement (element) {
  // $FlowFixMe[incompatible-return]: assume body is always available
  return ((isElement(element) ? element.ownerDocument // $FlowFixMe[prop-missing]
    : element.document) || window.document).documentElement
}

function getWindowScrollBarX (element) {
  // If <html> has a CSS width greater than the viewport, then this will be
  // incorrect for RTL.
  // Popper 1 is broken in this case and never had a bug report so let's assume
  // it's not an issue. I don't think anyone ever specifies width on <html>
  // anyway.
  // Browsers where the left scrollbar doesn't cause an issue report `0` for
  // this (e.g. Edge 2019, IE11, Safari)
  return getBoundingClientRect(getDocumentElement(element)).left + getWindowScroll(element).scrollLeft
}

function getComputedStyle (element) {
  return getWindow(element).getComputedStyle(element)
}

function isScrollParent (element) {
  // Firefox wants us to check `-x` and `-y` variations as well
  const _getComputedStyle = getComputedStyle(element)
  const overflow = _getComputedStyle.overflow
  const overflowX = _getComputedStyle.overflowX
  const overflowY = _getComputedStyle.overflowY

  return /auto|scroll|overlay|hidden/.test(overflow + overflowY + overflowX)
}

function isElementScaled (element) {
  const rect = element.getBoundingClientRect()
  const scaleX = rect.width / element.offsetWidth || 1
  const scaleY = rect.height / element.offsetHeight || 1
  return scaleX !== 1 || scaleY !== 1
} // Returns the composite rect of an element relative to its offsetParent.
// Composite means it takes into account transforms as well as layout.

function getCompositeRect (elementOrVirtualElement, offsetParent, isFixed) {
  if (isFixed === void 0) {
    isFixed = false
  }

  const isOffsetParentAnElement = isHTMLElement(offsetParent)
  const offsetParentIsScaled = isHTMLElement(offsetParent) && isElementScaled(offsetParent)
  const documentElement = getDocumentElement(offsetParent)
  const rect = getBoundingClientRect(elementOrVirtualElement, offsetParentIsScaled)
  let scroll = {
    scrollLeft: 0,
    scrollTop: 0
  }
  let offsets = {
    x: 0,
    y: 0
  }

  if (isOffsetParentAnElement || !isOffsetParentAnElement && !isFixed) {
    if (getNodeName(offsetParent) !== 'body' || // https://github.com/popperjs/popper-core/issues/1078
    isScrollParent(documentElement)) {
      scroll = getNodeScroll(offsetParent)
    }

    if (isHTMLElement(offsetParent)) {
      offsets = getBoundingClientRect(offsetParent, true)
      offsets.x += offsetParent.clientLeft
      offsets.y += offsetParent.clientTop
    } else if (documentElement) {
      offsets.x = getWindowScrollBarX(documentElement)
    }
  }

  return {
    x: rect.left + scroll.scrollLeft - offsets.x,
    y: rect.top + scroll.scrollTop - offsets.y,
    width: rect.width,
    height: rect.height
  }
}

// means it doesn't take into account transforms.

function getLayoutRect (element) {
  const clientRect = getBoundingClientRect(element) // Use the clientRect sizes if it's not been transformed.
  // Fixes https://github.com/popperjs/popper-core/issues/1223

  let width = element.offsetWidth
  let height = element.offsetHeight

  if (Math.abs(clientRect.width - width) <= 1) {
    width = clientRect.width
  }

  if (Math.abs(clientRect.height - height) <= 1) {
    height = clientRect.height
  }

  return {
    x: element.offsetLeft,
    y: element.offsetTop,
    width: width,
    height: height
  }
}

function getParentNode (element) {
  if (getNodeName(element) === 'html') {
    return element
  }

  return (// this is a quicker (but less type safe) way to save quite some bytes from the bundle
    // $FlowFixMe[incompatible-return]
    // $FlowFixMe[prop-missing]
    element.assignedSlot || // step into the shadow DOM of the parent of a slotted node
    element.parentNode || ( // DOM Element detected
      isShadowRoot(element) ? element.host : null) || // ShadowRoot detected
    // $FlowFixMe[incompatible-call]: HTMLElement is a Node
    getDocumentElement(element) // fallback

  )
}

function getScrollParent (node) {
  if (['html', 'body', '#document'].indexOf(getNodeName(node)) >= 0) {
    // $FlowFixMe[incompatible-return]: assume body is always available
    return node.ownerDocument.body
  }

  if (isHTMLElement(node) && isScrollParent(node)) {
    return node
  }

  return getScrollParent(getParentNode(node))
}

/*
given a DOM element, return the list of all scroll parents, up the list of ancesors
until we get to the top window object. This list is what we attach scroll listeners
to, because if any of these parent elements scroll, we'll need to re-calculate the
reference element's position.
*/

function listScrollParents (element, list) {
  let _element$ownerDocumen

  if (list === void 0) {
    list = []
  }

  const scrollParent = getScrollParent(element)
  const isBody = scrollParent === ((_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body)
  const win = getWindow(scrollParent)
  const target = isBody ? [win].concat(win.visualViewport || [], isScrollParent(scrollParent) ? scrollParent : []) : scrollParent
  const updatedList = list.concat(target)
  return isBody ? updatedList // $FlowFixMe[incompatible-call]: isBody tells us target will be an HTMLElement here
    : updatedList.concat(listScrollParents(getParentNode(target)))
}

function isTableElement (element) {
  return ['table', 'td', 'th'].indexOf(getNodeName(element)) >= 0
}

function getTrueOffsetParent (element) {
  if (!isHTMLElement(element) || // https://github.com/popperjs/popper-core/issues/837
  getComputedStyle(element).position === 'fixed') {
    return null
  }

  return element.offsetParent
} // `.offsetParent` reports `null` for fixed elements, while absolute elements
// return the containing block

function getContainingBlock (element) {
  const isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') !== -1
  const isIE = navigator.userAgent.indexOf('Trident') !== -1

  if (isIE && isHTMLElement(element)) {
    // In IE 9, 10 and 11 fixed elements containing block is always established by the viewport
    const elementCss = getComputedStyle(element)

    if (elementCss.position === 'fixed') {
      return null
    }
  }

  let currentNode = getParentNode(element)

  while (isHTMLElement(currentNode) && ['html', 'body'].indexOf(getNodeName(currentNode)) < 0) {
    const css = getComputedStyle(currentNode) // This is non-exhaustive but covers the most common CSS properties that
    // create a containing block.
    // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block#identifying_the_containing_block

    if (css.transform !== 'none' || css.perspective !== 'none' || css.contain === 'paint' || ['transform', 'perspective'].indexOf(css.willChange) !== -1 || isFirefox && css.willChange === 'filter' || isFirefox && css.filter && css.filter !== 'none') {
      return currentNode
    } else {
      currentNode = currentNode.parentNode
    }
  }

  return null
} // Gets the closest ancestor positioned element. Handles some edge cases,
// such as table ancestors and cross browser bugs.

function getOffsetParent (element) {
  const window = getWindow(element)
  let offsetParent = getTrueOffsetParent(element)

  while (offsetParent && isTableElement(offsetParent) && getComputedStyle(offsetParent).position === 'static') {
    offsetParent = getTrueOffsetParent(offsetParent)
  }

  if (offsetParent && (getNodeName(offsetParent) === 'html' || getNodeName(offsetParent) === 'body' && getComputedStyle(offsetParent).position === 'static')) {
    return window
  }

  return offsetParent || getContainingBlock(element) || window
}

const top = 'top'
const bottom = 'bottom'
const right = 'right'
const left = 'left'
const auto = 'auto'
const basePlacements = [top, bottom, right, left]
const start = 'start'
const end = 'end'
const clippingParents = 'clippingParents'
const viewport = 'viewport'
const popper = 'popper'
const reference = 'reference'

const beforeRead = 'beforeRead'
const read = 'read'
const afterRead = 'afterRead' // pure-logic modifiers

const beforeMain = 'beforeMain'
const main = 'main'
const afterMain = 'afterMain' // modifier with the purpose to write to the DOM (or write into a framework state)

const beforeWrite = 'beforeWrite'
const write = 'write'
const afterWrite = 'afterWrite'
const modifierPhases = [beforeRead, read, afterRead, beforeMain, main, afterMain, beforeWrite, write, afterWrite]

function order (modifiers) {
  const map = new Map()
  const visited = new Set()
  const result = []
  modifiers.forEach(function (modifier) {
    map.set(modifier.name, modifier)
  }) // On visiting object, check for its dependencies and visit them recursively

  function sort (modifier) {
    visited.add(modifier.name)
    const requires = [].concat(modifier.requires || [], modifier.requiresIfExists || [])
    requires.forEach(function (dep) {
      if (!visited.has(dep)) {
        const depModifier = map.get(dep)

        if (depModifier) {
          sort(depModifier)
        }
      }
    })
    result.push(modifier)
  }

  modifiers.forEach(function (modifier) {
    if (!visited.has(modifier.name)) {
      // check for visited object
      sort(modifier)
    }
  })
  return result
}

function orderModifiers (modifiers) {
  // order based on dependencies
  const orderedModifiers = order(modifiers) // order based on phase

  return modifierPhases.reduce(function (acc, phase) {
    return acc.concat(orderedModifiers.filter(function (modifier) {
      return modifier.phase === phase
    }))
  }, [])
}

function debounce (fn) {
  let pending
  return function () {
    if (!pending) {
      pending = new Promise(function (resolve) {
        Promise.resolve().then(function () {
          pending = undefined
          resolve(fn())
        })
      })
    }

    return pending
  }
}

function format (str) {
  for (var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
    args[_key - 1] = arguments[_key]
  }

  return [].concat(args).reduce(function (p, c) {
    return p.replace(/%s/, c)
  }, str)
}

const INVALID_MODIFIER_ERROR = 'Popper: modifier "%s" provided an invalid %s property, expected %s but got %s'
const MISSING_DEPENDENCY_ERROR = 'Popper: modifier "%s" requires "%s", but "%s" modifier is not available'
const VALID_PROPERTIES = ['name', 'enabled', 'phase', 'fn', 'effect', 'requires', 'options']
function validateModifiers (modifiers) {
  modifiers.forEach(function (modifier) {
    Object.keys(modifier).forEach(function (key) {
      switch (key) {
        case 'name':
          if (typeof modifier.name !== 'string') {
            console.error(format(INVALID_MODIFIER_ERROR, String(modifier.name), '"name"', '"string"', '"' + String(modifier.name) + '"'))
          }

          break

        case 'enabled':
          if (typeof modifier.enabled !== 'boolean') {
            console.error(format(INVALID_MODIFIER_ERROR, modifier.name, '"enabled"', '"boolean"', '"' + String(modifier.enabled) + '"'))
          }

        case 'phase':
          if (modifierPhases.indexOf(modifier.phase) < 0) {
            console.error(format(INVALID_MODIFIER_ERROR, modifier.name, '"phase"', 'either ' + modifierPhases.join(', '), '"' + String(modifier.phase) + '"'))
          }

          break

        case 'fn':
          if (typeof modifier.fn !== 'function') {
            console.error(format(INVALID_MODIFIER_ERROR, modifier.name, '"fn"', '"function"', '"' + String(modifier.fn) + '"'))
          }

          break

        case 'effect':
          if (typeof modifier.effect !== 'function') {
            console.error(format(INVALID_MODIFIER_ERROR, modifier.name, '"effect"', '"function"', '"' + String(modifier.fn) + '"'))
          }

          break

        case 'requires':
          if (!Array.isArray(modifier.requires)) {
            console.error(format(INVALID_MODIFIER_ERROR, modifier.name, '"requires"', '"array"', '"' + String(modifier.requires) + '"'))
          }

          break

        case 'requiresIfExists':
          if (!Array.isArray(modifier.requiresIfExists)) {
            console.error(format(INVALID_MODIFIER_ERROR, modifier.name, '"requiresIfExists"', '"array"', '"' + String(modifier.requiresIfExists) + '"'))
          }

          break

        case 'options':
        case 'data':
          break

        default:
          console.error('PopperJS: an invalid property has been provided to the "' + modifier.name + '" modifier, valid properties are ' + VALID_PROPERTIES.map(function (s) {
            return '"' + s + '"'
          }).join(', ') + '; but "' + key + '" was provided.')
      }

      modifier.requires && modifier.requires.forEach(function (requirement) {
        if (modifiers.find(function (mod) {
          return mod.name === requirement
        }) == null) {
          console.error(format(MISSING_DEPENDENCY_ERROR, String(modifier.name), requirement, requirement))
        }
      })
    })
  })
}

function uniqueBy (arr, fn) {
  const identifiers = new Set()
  return arr.filter(function (item) {
    const identifier = fn(item)

    if (!identifiers.has(identifier)) {
      identifiers.add(identifier)
      return true
    }
  })
}

function getBasePlacement (placement) {
  return placement.split('-')[0]
}

function mergeByName (modifiers) {
  const merged = modifiers.reduce(function (merged, current) {
    const existing = merged[current.name]
    merged[current.name] = existing ? Object.assign({}, existing, current, {
      options: Object.assign({}, existing.options, current.options),
      data: Object.assign({}, existing.data, current.data)
    }) : current
    return merged
  }, {}) // IE11 does not support Object.values

  return Object.keys(merged).map(function (key) {
    return merged[key]
  })
}

function getViewportRect (element) {
  const win = getWindow(element)
  const html = getDocumentElement(element)
  const visualViewport = win.visualViewport
  let width = html.clientWidth
  let height = html.clientHeight
  let x = 0
  let y = 0 // NB: This isn't supported on iOS <= 12. If the keyboard is open, the popper
  // can be obscured underneath it.
  // Also, `html.clientHeight` adds the bottom bar height in Safari iOS, even
  // if it isn't open, so if this isn't available, the popper will be detected
  // to overflow the bottom of the screen too early.

  if (visualViewport) {
    width = visualViewport.width
    height = visualViewport.height // Uses Layout Viewport (like Chrome; Safari does not currently)
    // In Chrome, it returns a value very close to 0 (+/-) but contains rounding
    // errors due to floating point numbers, so we need to check precision.
    // Safari returns a number <= 0, usually < -1 when pinch-zoomed
    // Feature detection fails in mobile emulation mode in Chrome.
    // Math.abs(win.innerWidth / visualViewport.scale - visualViewport.width) <
    // 0.001
    // Fallback here: "Not Safari" userAgent

    if (!/^((?!chrome|android).)*safari/i.test(navigator.userAgent)) {
      x = visualViewport.offsetLeft
      y = visualViewport.offsetTop
    }
  }

  return {
    width: width,
    height: height,
    x: x + getWindowScrollBarX(element),
    y: y
  }
}

const max = Math.max
const min = Math.min

// of the `<html>` and `<body>` rect bounds if horizontally scrollable

function getDocumentRect (element) {
  let _element$ownerDocumen

  const html = getDocumentElement(element)
  const winScroll = getWindowScroll(element)
  const body = (_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body
  const width = max(html.scrollWidth, html.clientWidth, body ? body.scrollWidth : 0, body ? body.clientWidth : 0)
  const height = max(html.scrollHeight, html.clientHeight, body ? body.scrollHeight : 0, body ? body.clientHeight : 0)
  let x = -winScroll.scrollLeft + getWindowScrollBarX(element)
  const y = -winScroll.scrollTop

  if (getComputedStyle(body || html).direction === 'rtl') {
    x += max(html.clientWidth, body ? body.clientWidth : 0) - width
  }

  return {
    width: width,
    height: height,
    x: x,
    y: y
  }
}

function contains (parent, child) {
  const rootNode = child.getRootNode && child.getRootNode() // First, attempt with faster native method

  if (parent.contains(child)) {
    return true
  } // then fallback to custom implementation with Shadow DOM support
  else if (rootNode && isShadowRoot(rootNode)) {
    let next = child

    do {
      if (next && parent.isSameNode(next)) {
        return true
      } // $FlowFixMe[prop-missing]: need a better way to handle this...

      next = next.parentNode || next.host
    } while (next)
  } // Give up, the result is false

  return false
}

function rectToClientRect (rect) {
  return Object.assign({}, rect, {
    left: rect.x,
    top: rect.y,
    right: rect.x + rect.width,
    bottom: rect.y + rect.height
  })
}

function getInnerBoundingClientRect (element) {
  const rect = getBoundingClientRect(element)
  rect.top = rect.top + element.clientTop
  rect.left = rect.left + element.clientLeft
  rect.bottom = rect.top + element.clientHeight
  rect.right = rect.left + element.clientWidth
  rect.width = element.clientWidth
  rect.height = element.clientHeight
  rect.x = rect.left
  rect.y = rect.top
  return rect
}

function getClientRectFromMixedType (element, clippingParent) {
  return clippingParent === viewport ? rectToClientRect(getViewportRect(element)) : isHTMLElement(clippingParent) ? getInnerBoundingClientRect(clippingParent) : rectToClientRect(getDocumentRect(getDocumentElement(element)))
} // A "clipping parent" is an overflowable container with the characteristic of
// clipping (or hiding) overflowing elements with a position different from
// `initial`

function getClippingParents (element) {
  const clippingParents = listScrollParents(getParentNode(element))
  const canEscapeClipping = ['absolute', 'fixed'].indexOf(getComputedStyle(element).position) >= 0
  const clipperElement = canEscapeClipping && isHTMLElement(element) ? getOffsetParent(element) : element

  if (!isElement(clipperElement)) {
    return []
  } // $FlowFixMe[incompatible-return]: https://github.com/facebook/flow/issues/1414

  return clippingParents.filter(function (clippingParent) {
    return isElement(clippingParent) && contains(clippingParent, clipperElement) && getNodeName(clippingParent) !== 'body'
  })
} // Gets the maximum area that the element is visible in due to any number of
// clipping parents

function getClippingRect (element, boundary, rootBoundary) {
  const mainClippingParents = boundary === 'clippingParents' ? getClippingParents(element) : [].concat(boundary)
  const clippingParents = [].concat(mainClippingParents, [rootBoundary])
  const firstClippingParent = clippingParents[0]
  const clippingRect = clippingParents.reduce(function (accRect, clippingParent) {
    const rect = getClientRectFromMixedType(element, clippingParent)
    accRect.top = max(rect.top, accRect.top)
    accRect.right = min(rect.right, accRect.right)
    accRect.bottom = min(rect.bottom, accRect.bottom)
    accRect.left = max(rect.left, accRect.left)
    return accRect
  }, getClientRectFromMixedType(element, firstClippingParent))
  clippingRect.width = clippingRect.right - clippingRect.left
  clippingRect.height = clippingRect.bottom - clippingRect.top
  clippingRect.x = clippingRect.left
  clippingRect.y = clippingRect.top
  return clippingRect
}

function getVariation (placement) {
  return placement.split('-')[1]
}

function getMainAxisFromPlacement (placement) {
  return ['top', 'bottom'].indexOf(placement) >= 0 ? 'x' : 'y'
}

function computeOffsets (_ref) {
  const reference = _ref.reference
  const element = _ref.element
  const placement = _ref.placement
  const basePlacement = placement ? getBasePlacement(placement) : null
  const variation = placement ? getVariation(placement) : null
  const commonX = reference.x + reference.width / 2 - element.width / 2
  const commonY = reference.y + reference.height / 2 - element.height / 2
  let offsets

  switch (basePlacement) {
    case top:
      offsets = {
        x: commonX,
        y: reference.y - element.height
      }
      break

    case bottom:
      offsets = {
        x: commonX,
        y: reference.y + reference.height
      }
      break

    case right:
      offsets = {
        x: reference.x + reference.width,
        y: commonY
      }
      break

    case left:
      offsets = {
        x: reference.x - element.width,
        y: commonY
      }
      break

    default:
      offsets = {
        x: reference.x,
        y: reference.y
      }
  }

  const mainAxis = basePlacement ? getMainAxisFromPlacement(basePlacement) : null

  if (mainAxis != null) {
    const len = mainAxis === 'y' ? 'height' : 'width'

    switch (variation) {
      case start:
        offsets[mainAxis] = offsets[mainAxis] - (reference[len] / 2 - element[len] / 2)
        break

      case end:
        offsets[mainAxis] = offsets[mainAxis] + (reference[len] / 2 - element[len] / 2)
        break
    }
  }

  return offsets
}

function getFreshSideObject () {
  return {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  }
}

function mergePaddingObject (paddingObject) {
  return Object.assign({}, getFreshSideObject(), paddingObject)
}

function expandToHashMap (value, keys) {
  return keys.reduce(function (hashMap, key) {
    hashMap[key] = value
    return hashMap
  }, {})
}

function detectOverflow (state, options) {
  if (options === void 0) {
    options = {}
  }

  const _options = options
  const _options$placement = _options.placement
  const placement = _options$placement === void 0 ? state.placement : _options$placement
  const _options$boundary = _options.boundary
  const boundary = _options$boundary === void 0 ? clippingParents : _options$boundary
  const _options$rootBoundary = _options.rootBoundary
  const rootBoundary = _options$rootBoundary === void 0 ? viewport : _options$rootBoundary
  const _options$elementConte = _options.elementContext
  const elementContext = _options$elementConte === void 0 ? popper : _options$elementConte
  const _options$altBoundary = _options.altBoundary
  const altBoundary = _options$altBoundary === void 0 ? false : _options$altBoundary
  const _options$padding = _options.padding
  const padding = _options$padding === void 0 ? 0 : _options$padding
  const paddingObject = mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements))
  const altContext = elementContext === popper ? reference : popper
  const referenceElement = state.elements.reference
  const popperRect = state.rects.popper
  const element = state.elements[altBoundary ? altContext : elementContext]
  const clippingClientRect = getClippingRect(isElement(element) ? element : element.contextElement || getDocumentElement(state.elements.popper), boundary, rootBoundary)
  const referenceClientRect = getBoundingClientRect(referenceElement)
  const popperOffsets = computeOffsets({
    reference: referenceClientRect,
    element: popperRect,
    strategy: 'absolute',
    placement: placement
  })
  const popperClientRect = rectToClientRect(Object.assign({}, popperRect, popperOffsets))
  const elementClientRect = elementContext === popper ? popperClientRect : referenceClientRect // positive = overflowing the clipping rect
  // 0 or negative = within the clipping rect

  const overflowOffsets = {
    top: clippingClientRect.top - elementClientRect.top + paddingObject.top,
    bottom: elementClientRect.bottom - clippingClientRect.bottom + paddingObject.bottom,
    left: clippingClientRect.left - elementClientRect.left + paddingObject.left,
    right: elementClientRect.right - clippingClientRect.right + paddingObject.right
  }
  const offsetData = state.modifiersData.offset // Offsets can be applied only to the popper element

  if (elementContext === popper && offsetData) {
    const offset = offsetData[placement]
    Object.keys(overflowOffsets).forEach(function (key) {
      const multiply = [right, bottom].indexOf(key) >= 0 ? 1 : -1
      const axis = [top, bottom].indexOf(key) >= 0 ? 'y' : 'x'
      overflowOffsets[key] += offset[axis] * multiply
    })
  }

  return overflowOffsets
}

const INVALID_ELEMENT_ERROR = 'Popper: Invalid reference or popper argument provided. They must be either a DOM element or virtual element.'
const INFINITE_LOOP_ERROR = 'Popper: An infinite loop in the modifiers cycle has been detected! The cycle has been interrupted to prevent a browser crash.'
const DEFAULT_OPTIONS = {
  placement: 'bottom',
  modifiers: [],
  strategy: 'absolute'
}

function areValidElements () {
  for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
    args[_key] = arguments[_key]
  }

  return !args.some(function (element) {
    return !(element && typeof element.getBoundingClientRect === 'function')
  })
}

function popperGenerator (generatorOptions) {
  if (generatorOptions === void 0) {
    generatorOptions = {}
  }

  const _generatorOptions = generatorOptions
  const _generatorOptions$def = _generatorOptions.defaultModifiers
  const defaultModifiers = _generatorOptions$def === void 0 ? [] : _generatorOptions$def
  const _generatorOptions$def2 = _generatorOptions.defaultOptions
  const defaultOptions = _generatorOptions$def2 === void 0 ? DEFAULT_OPTIONS : _generatorOptions$def2
  return function createPopper (reference, popper, options) {
    if (options === void 0) {
      options = defaultOptions
    }

    let state = {
      placement: 'bottom',
      orderedModifiers: [],
      options: Object.assign({}, DEFAULT_OPTIONS, defaultOptions),
      modifiersData: {},
      elements: {
        reference: reference,
        popper: popper
      },
      attributes: {},
      styles: {}
    }
    let effectCleanupFns = []
    let isDestroyed = false
    var instance = {
      state: state,
      setOptions: function setOptions (options) {
        cleanupModifierEffects()
        state.options = Object.assign({}, defaultOptions, state.options, options)
        state.scrollParents = {
          reference: isElement(reference) ? listScrollParents(reference) : reference.contextElement ? listScrollParents(reference.contextElement) : [],
          popper: listScrollParents(popper)
        } // Orders the modifiers based on their dependencies and `phase`
        // properties

        const orderedModifiers = orderModifiers(mergeByName([].concat(defaultModifiers, state.options.modifiers))) // Strip out disabled modifiers

        state.orderedModifiers = orderedModifiers.filter(function (m) {
          return m.enabled
        }) // Validate the provided modifiers so that the consumer will get warned
        // if one of the modifiers is invalid for any reason

        if (process.env.NODE_ENV !== 'production') {
          const modifiers = uniqueBy([].concat(orderedModifiers, state.options.modifiers), function (_ref) {
            const name = _ref.name
            return name
          })
          validateModifiers(modifiers)

          if (getBasePlacement(state.options.placement) === auto) {
            const flipModifier = state.orderedModifiers.find(function (_ref2) {
              const name = _ref2.name
              return name === 'flip'
            })

            if (!flipModifier) {
              console.error(['Popper: "auto" placements require the "flip" modifier be', 'present and enabled to work.'].join(' '))
            }
          }

          const _getComputedStyle = getComputedStyle(popper)
          const marginTop = _getComputedStyle.marginTop
          const marginRight = _getComputedStyle.marginRight
          const marginBottom = _getComputedStyle.marginBottom
          const marginLeft = _getComputedStyle.marginLeft // We no longer take into account `margins` on the popper, and it can
          // cause bugs with positioning, so we'll warn the consumer

          if ([marginTop, marginRight, marginBottom, marginLeft].some(function (margin) {
            return parseFloat(margin)
          })) {
            console.warn(['Popper: CSS "margin" styles cannot be used to apply padding', 'between the popper and its reference element or boundary.', 'To replicate margin, use the `offset` modifier, as well as', 'the `padding` option in the `preventOverflow` and `flip`', 'modifiers.'].join(' '))
          }
        }

        runModifierEffects()
        return instance.update()
      },
      // Sync update – it will always be executed, even if not necessary. This
      // is useful for low frequency updates where sync behavior simplifies the
      // logic.
      // For high frequency updates (e.g. `resize` and `scroll` events), always
      // prefer the async Popper#update method
      forceUpdate: function forceUpdate () {
        if (isDestroyed) {
          return
        }

        const _state$elements = state.elements
        const reference = _state$elements.reference
        const popper = _state$elements.popper // Don't proceed if `reference` or `popper` are not valid elements
        // anymore

        if (!areValidElements(reference, popper)) {
          if (process.env.NODE_ENV !== 'production') {
            console.error(INVALID_ELEMENT_ERROR)
          }

          return
        } // Store the reference and popper rects to be read by modifiers

        state.rects = {
          reference: getCompositeRect(reference, getOffsetParent(popper), state.options.strategy === 'fixed'),
          popper: getLayoutRect(popper)
        } // Modifiers have the ability to reset the current update cycle. The
        // most common use case for this is the `flip` modifier changing the
        // placement, which then needs to re-run all the modifiers, because the
        // logic was previously ran for the previous placement and is therefore
        // stale/incorrect

        state.reset = false
        state.placement = state.options.placement // On each update cycle, the `modifiersData` property for each modifier
        // is filled with the initial data specified by the modifier. This means
        // it doesn't persist and is fresh on each update.
        // To ensure persistent data, use `${name}#persistent`

        state.orderedModifiers.forEach(function (modifier) {
          return state.modifiersData[modifier.name] = Object.assign({}, modifier.data)
        })
        let __debug_loops__ = 0

        for (let index = 0; index < state.orderedModifiers.length; index++) {
          if (process.env.NODE_ENV !== 'production') {
            __debug_loops__ += 1

            if (__debug_loops__ > 100) {
              console.error(INFINITE_LOOP_ERROR)
              break
            }
          }

          if (state.reset === true) {
            state.reset = false
            index = -1
            continue
          }

          const _state$orderedModifie = state.orderedModifiers[index]
          const fn = _state$orderedModifie.fn
          const _state$orderedModifie2 = _state$orderedModifie.options
          const _options = _state$orderedModifie2 === void 0 ? {} : _state$orderedModifie2
          const name = _state$orderedModifie.name

          if (typeof fn === 'function') {
            state = fn({
              state: state,
              options: _options,
              name: name,
              instance: instance
            }) || state
          }
        }
      },
      // Async and optimistically optimized update – it will not be executed if
      // not necessary (debounced to run at most once-per-tick)
      update: debounce(function () {
        return new Promise(function (resolve) {
          instance.forceUpdate()
          resolve(state)
        })
      }),
      destroy: function destroy () {
        cleanupModifierEffects()
        isDestroyed = true
      }
    }

    if (!areValidElements(reference, popper)) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(INVALID_ELEMENT_ERROR)
      }

      return instance
    }

    instance.setOptions(options).then(function (state) {
      if (!isDestroyed && options.onFirstUpdate) {
        options.onFirstUpdate(state)
      }
    }) // Modifiers have the ability to execute arbitrary code before the first
    // update cycle runs. They will be executed in the same order as the update
    // cycle. This is useful when a modifier adds some persistent data that
    // other modifiers need to use, but the modifier is run after the dependent
    // one.

    function runModifierEffects () {
      state.orderedModifiers.forEach(function (_ref3) {
        const name = _ref3.name
        const _ref3$options = _ref3.options
        const options = _ref3$options === void 0 ? {} : _ref3$options
        const effect = _ref3.effect

        if (typeof effect === 'function') {
          const cleanupFn = effect({
            state: state,
            name: name,
            instance: instance,
            options: options
          })

          const noopFn = function noopFn () {}

          effectCleanupFns.push(cleanupFn || noopFn)
        }
      })
    }

    function cleanupModifierEffects () {
      effectCleanupFns.forEach(function (fn) {
        return fn()
      })
      effectCleanupFns = []
    }

    return instance
  }
}
const createPopper = /* #__PURE__ */popperGenerator() // eslint-disable-next-line import/no-unused-modules

exports.createPopper = createPopper
exports.detectOverflow = detectOverflow
exports.popperGenerator = popperGenerator
// # sourceMappingURL=popper-base.js.map
