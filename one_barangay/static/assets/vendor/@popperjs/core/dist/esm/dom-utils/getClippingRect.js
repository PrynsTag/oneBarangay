import { viewport } from '../enums.js'
import getViewportRect from './getViewportRect.js'
import getDocumentRect from './getDocumentRect.js'
import listScrollParents from './listScrollParents.js'
import getOffsetParent from './getOffsetParent.js'
import getDocumentElement from './getDocumentElement.js'
import getComputedStyle from './getComputedStyle.js'
import { isElement, isHTMLElement } from './instanceOf.js'
import getBoundingClientRect from './getBoundingClientRect.js'
import getParentNode from './getParentNode.js'
import contains from './contains.js'
import getNodeName from './getNodeName.js'
import rectToClientRect from '../utils/rectToClientRect.js'
import { max, min } from '../utils/math.js'

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

export default function getClippingRect (element, boundary, rootBoundary) {
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
