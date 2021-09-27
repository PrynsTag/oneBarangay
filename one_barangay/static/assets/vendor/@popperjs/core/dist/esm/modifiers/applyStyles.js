import getNodeName from '../dom-utils/getNodeName.js'
import { isHTMLElement } from '../dom-utils/instanceOf.js' // This modifier takes the styles prepared by the `computeStyles` modifier
// and applies them to the HTMLElements such as popper and arrow

function applyStyles (_ref) {
  const state = _ref.state
  Object.keys(state.elements).forEach(function (name) {
    const style = state.styles[name] || {}
    const attributes = state.attributes[name] || {}
    const element = state.elements[name] // arrow is optional + virtual elements

    if (!isHTMLElement(element) || !getNodeName(element)) {
      return
    } // Flow doesn't support to extend this property, but it's the most
    // effective way to apply styles to an HTMLElement
    // $FlowFixMe[cannot-write]

    Object.assign(element.style, style)
    Object.keys(attributes).forEach(function (name) {
      const value = attributes[name]

      if (value === false) {
        element.removeAttribute(name)
      } else {
        element.setAttribute(name, value === true ? '' : value)
      }
    })
  })
}

function effect (_ref2) {
  const state = _ref2.state
  const initialStyles = {
    popper: {
      position: state.options.strategy,
      left: '0',
      top: '0',
      margin: '0'
    },
    arrow: {
      position: 'absolute'
    },
    reference: {}
  }
  Object.assign(state.elements.popper.style, initialStyles.popper)
  state.styles = initialStyles

  if (state.elements.arrow) {
    Object.assign(state.elements.arrow.style, initialStyles.arrow)
  }

  return function () {
    Object.keys(state.elements).forEach(function (name) {
      const element = state.elements[name]
      const attributes = state.attributes[name] || {}
      const styleProperties = Object.keys(state.styles.hasOwnProperty(name) ? state.styles[name] : initialStyles[name]) // Set all values to an empty string to unset them

      const style = styleProperties.reduce(function (style, property) {
        style[property] = ''
        return style
      }, {}) // arrow is optional + virtual elements

      if (!isHTMLElement(element) || !getNodeName(element)) {
        return
      }

      Object.assign(element.style, style)
      Object.keys(attributes).forEach(function (attribute) {
        element.removeAttribute(attribute)
      })
    })
  }
} // eslint-disable-next-line import/no-unused-modules

export default {
  name: 'applyStyles',
  enabled: true,
  phase: 'write',
  fn: applyStyles,
  effect: effect,
  requires: ['computeStyles']
}
