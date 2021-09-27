import { top, left, right, bottom } from '../enums.js'
import getOffsetParent from '../dom-utils/getOffsetParent.js'
import getWindow from '../dom-utils/getWindow.js'
import getDocumentElement from '../dom-utils/getDocumentElement.js'
import getComputedStyle from '../dom-utils/getComputedStyle.js'
import getBasePlacement from '../utils/getBasePlacement.js'
import { round } from '../utils/math.js' // eslint-disable-next-line import/no-unused-modules

const unsetSides = {
  top: 'auto',
  right: 'auto',
  bottom: 'auto',
  left: 'auto'
} // Round the offsets to the nearest suitable subpixel based on the DPR.
// Zooming can change the DPR, but it seems to report a value that will
// cleanly divide the values into the appropriate subpixels.

function roundOffsetsByDPR (_ref) {
  const x = _ref.x
  const y = _ref.y
  const win = window
  const dpr = win.devicePixelRatio || 1
  return {
    x: round(round(x * dpr) / dpr) || 0,
    y: round(round(y * dpr) / dpr) || 0
  }
}

export function mapToStyles (_ref2) {
  let _Object$assign2

  const popper = _ref2.popper
  const popperRect = _ref2.popperRect
  const placement = _ref2.placement
  const offsets = _ref2.offsets
  const position = _ref2.position
  const gpuAcceleration = _ref2.gpuAcceleration
  const adaptive = _ref2.adaptive
  const roundOffsets = _ref2.roundOffsets

  const _ref3 = roundOffsets === true ? roundOffsetsByDPR(offsets) : typeof roundOffsets === 'function' ? roundOffsets(offsets) : offsets
  const _ref3$x = _ref3.x
  let x = _ref3$x === void 0 ? 0 : _ref3$x
  const _ref3$y = _ref3.y
  let y = _ref3$y === void 0 ? 0 : _ref3$y

  const hasX = offsets.hasOwnProperty('x')
  const hasY = offsets.hasOwnProperty('y')
  let sideX = left
  let sideY = top
  const win = window

  if (adaptive) {
    let offsetParent = getOffsetParent(popper)
    let heightProp = 'clientHeight'
    let widthProp = 'clientWidth'

    if (offsetParent === getWindow(popper)) {
      offsetParent = getDocumentElement(popper)

      if (getComputedStyle(offsetParent).position !== 'static') {
        heightProp = 'scrollHeight'
        widthProp = 'scrollWidth'
      }
    } // $FlowFixMe[incompatible-cast]: force type refinement, we compare offsetParent with window above, but Flow doesn't detect it

    offsetParent = offsetParent

    if (placement === top) {
      sideY = bottom // $FlowFixMe[prop-missing]

      y -= offsetParent[heightProp] - popperRect.height
      y *= gpuAcceleration ? 1 : -1
    }

    if (placement === left) {
      sideX = right // $FlowFixMe[prop-missing]

      x -= offsetParent[widthProp] - popperRect.width
      x *= gpuAcceleration ? 1 : -1
    }
  }

  const commonStyles = Object.assign({
    position: position
  }, adaptive && unsetSides)

  if (gpuAcceleration) {
    let _Object$assign

    return Object.assign({}, commonStyles, (_Object$assign = {}, _Object$assign[sideY] = hasY ? '0' : '', _Object$assign[sideX] = hasX ? '0' : '', _Object$assign.transform = (win.devicePixelRatio || 1) < 2 ? 'translate(' + x + 'px, ' + y + 'px)' : 'translate3d(' + x + 'px, ' + y + 'px, 0)', _Object$assign))
  }

  return Object.assign({}, commonStyles, (_Object$assign2 = {}, _Object$assign2[sideY] = hasY ? y + 'px' : '', _Object$assign2[sideX] = hasX ? x + 'px' : '', _Object$assign2.transform = '', _Object$assign2))
}

function computeStyles (_ref4) {
  const state = _ref4.state
  const options = _ref4.options
  const _options$gpuAccelerat = options.gpuAcceleration
  const gpuAcceleration = _options$gpuAccelerat === void 0 ? true : _options$gpuAccelerat
  const _options$adaptive = options.adaptive
  const adaptive = _options$adaptive === void 0 ? true : _options$adaptive
  const _options$roundOffsets = options.roundOffsets
  const roundOffsets = _options$roundOffsets === void 0 ? true : _options$roundOffsets

  if (false) {
    const transitionProperty = getComputedStyle(state.elements.popper).transitionProperty || ''

    if (adaptive && ['transform', 'top', 'right', 'bottom', 'left'].some(function (property) {
      return transitionProperty.indexOf(property) >= 0
    })) {
      console.warn(['Popper: Detected CSS transitions on at least one of the following', 'CSS properties: "transform", "top", "right", "bottom", "left".', '\n\n', 'Disable the "computeStyles" modifier\'s `adaptive` option to allow', 'for smooth transitions, or remove these properties from the CSS', 'transition declaration on the popper element if only transitioning', 'opacity or background-color for example.', '\n\n', 'We recommend using the popper element as a wrapper around an inner', 'element that can have any CSS property transitioned for animations.'].join(' '))
    }
  }

  const commonStyles = {
    placement: getBasePlacement(state.placement),
    popper: state.elements.popper,
    popperRect: state.rects.popper,
    gpuAcceleration: gpuAcceleration
  }

  if (state.modifiersData.popperOffsets != null) {
    state.styles.popper = Object.assign({}, state.styles.popper, mapToStyles(Object.assign({}, commonStyles, {
      offsets: state.modifiersData.popperOffsets,
      position: state.options.strategy,
      adaptive: adaptive,
      roundOffsets: roundOffsets
    })))
  }

  if (state.modifiersData.arrow != null) {
    state.styles.arrow = Object.assign({}, state.styles.arrow, mapToStyles(Object.assign({}, commonStyles, {
      offsets: state.modifiersData.arrow,
      position: 'absolute',
      adaptive: false,
      roundOffsets: roundOffsets
    })))
  }

  state.attributes.popper = Object.assign({}, state.attributes.popper, {
    'data-popper-placement': state.placement
  })
} // eslint-disable-next-line import/no-unused-modules

export default {
  name: 'computeStyles',
  enabled: true,
  phase: 'beforeWrite',
  fn: computeStyles,
  data: {}
}
