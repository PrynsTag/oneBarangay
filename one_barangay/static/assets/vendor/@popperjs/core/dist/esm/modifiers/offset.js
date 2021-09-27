import getBasePlacement from '../utils/getBasePlacement.js'
import { top, left, right, placements } from '../enums.js'
export function distanceAndSkiddingToXY (placement, rects, offset) {
  const basePlacement = getBasePlacement(placement)
  const invertDistance = [left, top].indexOf(basePlacement) >= 0 ? -1 : 1

  const _ref = typeof offset === 'function' ? offset(Object.assign({}, rects, {
    placement: placement
  })) : offset
  let skidding = _ref[0]
  let distance = _ref[1]

  skidding = skidding || 0
  distance = (distance || 0) * invertDistance
  return [left, right].indexOf(basePlacement) >= 0 ? {
    x: distance,
    y: skidding
  } : {
    x: skidding,
    y: distance
  }
}

function offset (_ref2) {
  const state = _ref2.state
  const options = _ref2.options
  const name = _ref2.name
  const _options$offset = options.offset
  const offset = _options$offset === void 0 ? [0, 0] : _options$offset
  const data = placements.reduce(function (acc, placement) {
    acc[placement] = distanceAndSkiddingToXY(placement, state.rects, offset)
    return acc
  }, {})
  const _data$state$placement = data[state.placement]
  const x = _data$state$placement.x
  const y = _data$state$placement.y

  if (state.modifiersData.popperOffsets != null) {
    state.modifiersData.popperOffsets.x += x
    state.modifiersData.popperOffsets.y += y
  }

  state.modifiersData[name] = data
} // eslint-disable-next-line import/no-unused-modules

export default {
  name: 'offset',
  enabled: true,
  phase: 'main',
  requires: ['popperOffsets'],
  fn: offset
}
