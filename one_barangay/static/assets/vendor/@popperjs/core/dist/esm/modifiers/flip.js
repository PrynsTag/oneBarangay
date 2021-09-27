import getOppositePlacement from '../utils/getOppositePlacement.js'
import getBasePlacement from '../utils/getBasePlacement.js'
import getOppositeVariationPlacement from '../utils/getOppositeVariationPlacement.js'
import detectOverflow from '../utils/detectOverflow.js'
import computeAutoPlacement from '../utils/computeAutoPlacement.js'
import { bottom, top, start, right, left, auto } from '../enums.js'
import getVariation from '../utils/getVariation.js' // eslint-disable-next-line import/no-unused-modules

function getExpandedFallbackPlacements (placement) {
  if (getBasePlacement(placement) === auto) {
    return []
  }

  const oppositePlacement = getOppositePlacement(placement)
  return [getOppositeVariationPlacement(placement), oppositePlacement, getOppositeVariationPlacement(oppositePlacement)]
}

function flip (_ref) {
  const state = _ref.state
  const options = _ref.options
  const name = _ref.name

  if (state.modifiersData[name]._skip) {
    return
  }

  const _options$mainAxis = options.mainAxis
  const checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis
  const _options$altAxis = options.altAxis
  const checkAltAxis = _options$altAxis === void 0 ? true : _options$altAxis
  const specifiedFallbackPlacements = options.fallbackPlacements
  const padding = options.padding
  const boundary = options.boundary
  const rootBoundary = options.rootBoundary
  const altBoundary = options.altBoundary
  const _options$flipVariatio = options.flipVariations
  const flipVariations = _options$flipVariatio === void 0 ? true : _options$flipVariatio
  const allowedAutoPlacements = options.allowedAutoPlacements
  const preferredPlacement = state.options.placement
  const basePlacement = getBasePlacement(preferredPlacement)
  const isBasePlacement = basePlacement === preferredPlacement
  const fallbackPlacements = specifiedFallbackPlacements || (isBasePlacement || !flipVariations ? [getOppositePlacement(preferredPlacement)] : getExpandedFallbackPlacements(preferredPlacement))
  const placements = [preferredPlacement].concat(fallbackPlacements).reduce(function (acc, placement) {
    return acc.concat(getBasePlacement(placement) === auto ? computeAutoPlacement(state, {
      placement: placement,
      boundary: boundary,
      rootBoundary: rootBoundary,
      padding: padding,
      flipVariations: flipVariations,
      allowedAutoPlacements: allowedAutoPlacements
    }) : placement)
  }, [])
  const referenceRect = state.rects.reference
  const popperRect = state.rects.popper
  const checksMap = new Map()
  let makeFallbackChecks = true
  let firstFittingPlacement = placements[0]

  for (let i = 0; i < placements.length; i++) {
    const placement = placements[i]

    const _basePlacement = getBasePlacement(placement)

    const isStartVariation = getVariation(placement) === start
    const isVertical = [top, bottom].indexOf(_basePlacement) >= 0
    const len = isVertical ? 'width' : 'height'
    const overflow = detectOverflow(state, {
      placement: placement,
      boundary: boundary,
      rootBoundary: rootBoundary,
      altBoundary: altBoundary,
      padding: padding
    })
    let mainVariationSide = isVertical ? isStartVariation ? right : left : isStartVariation ? bottom : top

    if (referenceRect[len] > popperRect[len]) {
      mainVariationSide = getOppositePlacement(mainVariationSide)
    }

    const altVariationSide = getOppositePlacement(mainVariationSide)
    const checks = []

    if (checkMainAxis) {
      checks.push(overflow[_basePlacement] <= 0)
    }

    if (checkAltAxis) {
      checks.push(overflow[mainVariationSide] <= 0, overflow[altVariationSide] <= 0)
    }

    if (checks.every(function (check) {
      return check
    })) {
      firstFittingPlacement = placement
      makeFallbackChecks = false
      break
    }

    checksMap.set(placement, checks)
  }

  if (makeFallbackChecks) {
    // `2` may be desired in some cases – research later
    const numberOfChecks = flipVariations ? 3 : 1

    const _loop = function _loop (_i) {
      const fittingPlacement = placements.find(function (placement) {
        const checks = checksMap.get(placement)

        if (checks) {
          return checks.slice(0, _i).every(function (check) {
            return check
          })
        }
      })

      if (fittingPlacement) {
        firstFittingPlacement = fittingPlacement
        return 'break'
      }
    }

    for (let _i = numberOfChecks; _i > 0; _i--) {
      const _ret = _loop(_i)

      if (_ret === 'break') break
    }
  }

  if (state.placement !== firstFittingPlacement) {
    state.modifiersData[name]._skip = true
    state.placement = firstFittingPlacement
    state.reset = true
  }
} // eslint-disable-next-line import/no-unused-modules

export default {
  name: 'flip',
  enabled: true,
  phase: 'main',
  fn: flip,
  requiresIfExists: ['offset'],
  data: {
    _skip: false
  }
}
