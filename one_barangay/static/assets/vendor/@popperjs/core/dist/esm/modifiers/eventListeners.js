import getWindow from '../dom-utils/getWindow.js' // eslint-disable-next-line import/no-unused-modules

const passive = {
  passive: true
}

function effect (_ref) {
  const state = _ref.state
  const instance = _ref.instance
  const options = _ref.options
  const _options$scroll = options.scroll
  const scroll = _options$scroll === void 0 ? true : _options$scroll
  const _options$resize = options.resize
  const resize = _options$resize === void 0 ? true : _options$resize
  const window = getWindow(state.elements.popper)
  const scrollParents = [].concat(state.scrollParents.reference, state.scrollParents.popper)

  if (scroll) {
    scrollParents.forEach(function (scrollParent) {
      scrollParent.addEventListener('scroll', instance.update, passive)
    })
  }

  if (resize) {
    window.addEventListener('resize', instance.update, passive)
  }

  return function () {
    if (scroll) {
      scrollParents.forEach(function (scrollParent) {
        scrollParent.removeEventListener('scroll', instance.update, passive)
      })
    }

    if (resize) {
      window.removeEventListener('resize', instance.update, passive)
    }
  }
} // eslint-disable-next-line import/no-unused-modules

export default {
  name: 'eventListeners',
  enabled: true,
  phase: 'write',
  fn: function fn () {},
  effect: effect,
  data: {}
}
