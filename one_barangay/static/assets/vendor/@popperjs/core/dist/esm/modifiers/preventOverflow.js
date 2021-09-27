import { top, left, right, bottom, start } from '../enums.js'
import getBasePlacement from '../utils/getBasePlacement.js'
import getMainAxisFromPlacement from '../utils/getMainAxisFromPlacement.js'
import getAltAxis from '../utils/getAltAxis.js'
import within from '../utils/within.js'
import getLayoutRect from '../dom-utils/getLayoutRect.js'
import getOffsetParent from '../dom-utils/getOffsetParent.js'
import detectOverflow from '../utils/detectOverflow.js'
import getVariation from '../utils/getVariation.js'
import getFreshSideObject from '../utils/getFreshSideObject.js'
import { max as mathMax, min as mathMin } from '../utils/math.js'

function preventOverflow (_ref) {
  const state = _ref.state
  const options = _ref.options
  const name = _ref.name
  const _options$mainAxis = options.mainAxis
  const checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis
  const _options$altAxis = options.altAxis
  const checkAltAxis = _options$altAxis === void 0 ? false : _options$altAxis
  const boundary = options.boundary
  const rootBoundary = options.rootBoundary
  const altBoundary = options.altBoundary
  const padding = options.padding
  const _options$tether = options.tether
  const tether = _options$tether === void 0 ? true : _options$tether
  const _options$tetherOffset = options.tetherOffset
  const tetherOffset = _options$tetherOffset === void 0 ? 0 : _options$tetherOffset
  const overflow = detectOverflow(state, {
    boundary: boundary,
    rootBoundary: rootBoundary,
    padding: padding,
    altBoundary: altBoundary
  })
  const basePlacement = getBasePlacement(state.placement)
  const variation = getVariation(state.placement)
  const isBasePlacement = !variation
  const mainAxis = getMainAxisFromPlacement(basePlacement)
  const altAxis = getAltAxis(mainAxis)
  const popperOffsets = state.modifiersData.popperOffsets
  const referenceRect = state.rects.reference
  const popperRect = state.rects.popper
  const tetherOffsetValue = typeof tetherOffset === 'function' ? tetherOffset(Object.assign({}, state.rects, {
    placement: state.placement
  })) : tetherOffset
  const data = {
    x: 0,
    y: 0
  }

  if (!popperOffsets) {
    return
  }

  if (checkMainAxis || checkAltAxis) {
    const mainSide = mainAxis === 'y' ? top : left
    const altSide = mainAxis === 'y' ? bottom : right
    const len = mainAxis === 'y' ? 'height' : 'width'
    const offset = popperOffsets[mainAxis]
    const min = popperOffsets[mainAxis] + overflow[mainSide]
    const max = popperOffsets[mainAxis] - overflow[altSide]
    const additive = tether ? -popperRect[len] / 2 : 0
    const minLen = variation === start ? referenceRect[len] : popperRect[len]
    const maxLen = variation === start ? -popperRect[len] : -referenceRect[len] // We need to include the arrow in the calculation so the arrow doesn't go
    // outside the reference bounds

    const arrowElement = state.elements.arrow
    const arrowRect = tether && arrowElement ? getLayoutRect(arrowElement) : {
      width: 0,
      height: 0
    }
    const arrowPaddingObject = state.modifiersData['arrow#persistent'] ? state.modifiersData['arrow#persistent'].padding : getFreshSideObject()
    const arrowPaddingMin = arrowPaddingObject[mainSide]
    const arrowPaddingMax = arrowPaddingObject[altSide] // If the reference length is smaller than the arrow length, we don't want
    // to include its full size in the calculation. If the reference is small
    // and near the edge of a boundary, the popper can overflow even if the
    // reference is not overflowing as well (e.g. virtual elements with no
    // width or height)

    const arrowLen = within(0, referenceRect[len], arrowRect[len])
    const minOffset = isBasePlacement ? referenceRect[len] / 2 - additive - arrowLen - arrowPaddingMin - tetherOffsetValue : minLen - arrowLen - arrowPaddingMin - tetherOffsetValue
    const maxOffset = isBasePlacement ? -referenceRect[len] / 2 + additive + arrowLen + arrowPaddingMax + tetherOffsetValue : maxLen + arrowLen + arrowPaddingMax + tetherOffsetValue
    const arrowOffsetParent = state.elements.arrow && getOffsetParent(state.elements.arrow)
    const clientOffset = arrowOffsetParent ? mainAxis === 'y' ? arrowOffsetParent.clientTop || 0 : arrowOffsetParent.clientLeft || 0 : 0
    const offsetModifierValue = state.modifiersData.offset ? state.modifiersData.offset[state.placement][mainAxis] : 0
    const tetherMin = popperOffsets[mainAxis] + minOffset - offsetModifierValue - clientOffset
    const tetherMax = popperOffsets[mainAxis] + maxOffset - offsetModifierValue

    if (checkMainAxis) {
      const preventedOffset = within(tether ? mathMin(min, tetherMin) : min, offset, tether ? mathMax(max, tetherMax) : max)
      popperOffsets[mainAxis] = preventedOffset
      data[mainAxis] = preventedOffset - offset
    }

    if (checkAltAxis) {
      const _mainSide = mainAxis === 'x' ? top : left

      const _altSide = mainAxis === 'x' ? bottom : right

      const _offset = popperOffsets[altAxis]

      const _min = _offset + overflow[_mainSide]

      const _max = _offset - overflow[_altSide]

      const _preventedOffset = within(tether ? mathMin(_min, tetherMin) : _min, _offset, tether ? mathMax(_max, tetherMax) : _max)

      popperOffsets[altAxis] = _preventedOffset
      data[altAxis] = _preventedOffset - _offset
    }
  }

  state.modifiersData[name] = data
} // eslint-disable-next-line import/no-unused-modules

export default {
  name: 'preventOverflow',
  enabled: true,
  phase: 'main',
  fn: preventOverflow,
  requiresIfExists: ['offset']
}
