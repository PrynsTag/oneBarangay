/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

var __assign = function () {
  __assign =
    Object.assign ||
    function __assign (t) {
      for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i]
        for (const p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p]
      }
      return t
    }
  return __assign.apply(this, arguments)
}

const NotyfNotification = /** @class */ (function () {
  function NotyfNotification (options) {
    this.options = options
    this.listeners = {}
  }
  NotyfNotification.prototype.on = function (eventType, cb) {
    const callbacks = this.listeners[eventType] || []
    this.listeners[eventType] = callbacks.concat([cb])
  }
  NotyfNotification.prototype.triggerEvent = function (eventType, event) {
    const _this = this
    const callbacks = this.listeners[eventType] || []
    callbacks.forEach(function (cb) {
      return cb({ target: _this, event: event })
    })
  }
  return NotyfNotification
})()
let NotyfArrayEvent;
(function (NotyfArrayEvent) {
  NotyfArrayEvent[(NotyfArrayEvent.Add = 0)] = 'Add'
  NotyfArrayEvent[(NotyfArrayEvent.Remove = 1)] = 'Remove'
})(NotyfArrayEvent || (NotyfArrayEvent = {}))
const NotyfArray = /** @class */ (function () {
  function NotyfArray () {
    this.notifications = []
  }
  NotyfArray.prototype.push = function (elem) {
    this.notifications.push(elem)
    this.updateFn(elem, NotyfArrayEvent.Add, this.notifications)
  }
  NotyfArray.prototype.splice = function (index, num) {
    const elem = this.notifications.splice(index, num)[0]
    this.updateFn(elem, NotyfArrayEvent.Remove, this.notifications)
    return elem
  }
  NotyfArray.prototype.indexOf = function (elem) {
    return this.notifications.indexOf(elem)
  }
  NotyfArray.prototype.onUpdate = function (fn) {
    this.updateFn = fn
  }
  return NotyfArray
})()

let NotyfEvent;
(function (NotyfEvent) {
  NotyfEvent.Dismiss = 'dismiss'
  NotyfEvent.Click = 'click'
})(NotyfEvent || (NotyfEvent = {}))
const DEFAULT_OPTIONS = {
  types: [
    {
      type: 'success',
      className: 'notyf__toast--success',
      backgroundColor: '#3dc763',
      icon: {
        className: 'notyf__icon--success',
        tagName: 'i'
      }
    },
    {
      type: 'error',
      className: 'notyf__toast--error',
      backgroundColor: '#ed3d3d',
      icon: {
        className: 'notyf__icon--error',
        tagName: 'i'
      }
    }
  ],
  duration: 2000,
  ripple: true,
  position: {
    x: 'right',
    y: 'bottom'
  },
  dismissible: false
}

const NotyfView = /** @class */ (function () {
  function NotyfView () {
    this.notifications = []
    this.events = {}
    this.X_POSITION_FLEX_MAP = {
      left: 'flex-start',
      center: 'center',
      right: 'flex-end'
    }
    this.Y_POSITION_FLEX_MAP = {
      top: 'flex-start',
      center: 'center',
      bottom: 'flex-end'
    }
    // Creates the main notifications container
    const docFrag = document.createDocumentFragment()
    const notyfContainer = this._createHTMLElement({ tagName: 'div', className: 'notyf' })
    docFrag.appendChild(notyfContainer)
    document.body.appendChild(docFrag)
    this.container = notyfContainer
    // Identifies the main animation end event
    this.animationEndEventName = this._getAnimationEndEventName()
    this._createA11yContainer()
  }
  NotyfView.prototype.on = function (event, cb) {
    let _a
    this.events = __assign(__assign({}, this.events), ((_a = {}), (_a[event] = cb), _a))
  }
  NotyfView.prototype.update = function (notification, type) {
    if (type === NotyfArrayEvent.Add) {
      this.addNotification(notification)
    } else if (type === NotyfArrayEvent.Remove) {
      this.removeNotification(notification)
    }
  }
  NotyfView.prototype.removeNotification = function (notification) {
    const _this = this
    const renderedNotification = this._popRenderedNotification(notification)
    let node
    if (!renderedNotification) {
      return
    }
    node = renderedNotification.node
    node.classList.add('notyf__toast--disappear')
    let handleEvent
    node.addEventListener(
      this.animationEndEventName,
      (handleEvent = function (event) {
        if (event.target === node) {
          node.removeEventListener(_this.animationEndEventName, handleEvent)
          _this.container.removeChild(node)
        }
      })
    )
  }
  NotyfView.prototype.addNotification = function (notification) {
    const node = this._renderNotification(notification)
    this.notifications.push({ notification: notification, node: node })
    // For a11y purposes, we still want to announce that there's a notification in the screen
    // even if it comes with no message.
    this._announce(notification.options.message || 'Notification')
  }
  NotyfView.prototype._renderNotification = function (notification) {
    let _a
    const card = this._buildNotificationCard(notification)
    const className = notification.options.className
    if (className) {
      (_a = card.classList).add.apply(_a, className.split(' '))
    }
    this.container.appendChild(card)
    return card
  }
  NotyfView.prototype._popRenderedNotification = function (notification) {
    let idx = -1
    for (let i = 0; i < this.notifications.length && idx < 0; i++) {
      if (this.notifications[i].notification === notification) {
        idx = i
      }
    }
    if (idx !== -1) {
      return this.notifications.splice(idx, 1)[0]
    }
  }
  NotyfView.prototype.getXPosition = function (options) {
    let _a
    return (
      ((_a = options === null || options === void 0 ? void 0 : options.position) === null || _a === void 0
        ? void 0
        : _a.x) || 'right'
    )
  }
  NotyfView.prototype.getYPosition = function (options) {
    let _a
    return (
      ((_a = options === null || options === void 0 ? void 0 : options.position) === null || _a === void 0
        ? void 0
        : _a.y) || 'bottom'
    )
  }
  NotyfView.prototype.adjustContainerAlignment = function (options) {
    const align = this.X_POSITION_FLEX_MAP[this.getXPosition(options)]
    const justify = this.Y_POSITION_FLEX_MAP[this.getYPosition(options)]
    const style = this.container.style
    style.setProperty('justify-content', justify)
    style.setProperty('align-items', align)
  }
  NotyfView.prototype._buildNotificationCard = function (notification) {
    const _this = this
    const options = notification.options
    const iconOpts = options.icon
    // Adjust container according to position (e.g. top-left, bottom-center, etc)
    this.adjustContainerAlignment(options)
    // Create elements
    const notificationElem = this._createHTMLElement({ tagName: 'div', className: 'notyf__toast' })
    const ripple = this._createHTMLElement({ tagName: 'div', className: 'notyf__ripple' })
    const wrapper = this._createHTMLElement({ tagName: 'div', className: 'notyf__wrapper' })
    const message = this._createHTMLElement({ tagName: 'div', className: 'notyf__message' })
    message.innerHTML = options.message || ''
    const mainColor = options.background || options.backgroundColor
    // Build the icon and append it to the card
    if (iconOpts) {
      const iconContainer = this._createHTMLElement({ tagName: 'div', className: 'notyf__icon' })
      if (typeof iconOpts === 'string' || iconOpts instanceof String) {
        iconContainer.innerHTML = new String(iconOpts).valueOf()
      }
      if (typeof iconOpts === 'object') {
        const _a = iconOpts.tagName
        const tagName = _a === void 0 ? 'i' : _a
        const className_1 = iconOpts.className
        const text = iconOpts.text
        const _b = iconOpts.color
        const color = _b === void 0 ? mainColor : _b
        const iconElement = this._createHTMLElement({ tagName: tagName, className: className_1, text: text })
        if (color) {
          iconElement.style.color = color
        }
        iconContainer.appendChild(iconElement)
      }
      wrapper.appendChild(iconContainer)
    }
    wrapper.appendChild(message)
    notificationElem.appendChild(wrapper)
    // Add ripple if applicable, else just paint the full toast
    if (mainColor) {
      if (options.ripple) {
        ripple.style.background = mainColor
        notificationElem.appendChild(ripple)
      } else {
        notificationElem.style.background = mainColor
      }
    }
    // Add dismiss button
    if (options.dismissible) {
      const dismissWrapper = this._createHTMLElement({ tagName: 'div', className: 'notyf__dismiss' })
      const dismissButton = this._createHTMLElement({
        tagName: 'button',
        className: 'notyf__dismiss-btn'
      })
      dismissWrapper.appendChild(dismissButton)
      wrapper.appendChild(dismissWrapper)
      notificationElem.classList.add('notyf__toast--dismissible')
      dismissButton.addEventListener('click', function (event) {
        let _a, _b;
        (_b = (_a = _this.events)[NotyfEvent.Dismiss]) === null || _b === void 0
          ? void 0
          : _b.call(_a, { target: notification, event: event })
        event.stopPropagation()
      })
    }
    notificationElem.addEventListener('click', function (event) {
      let _a, _b
      return (_b = (_a = _this.events)[NotyfEvent.Click]) === null || _b === void 0
        ? void 0
        : _b.call(_a, { target: notification, event: event })
    })
    // Adjust margins depending on whether its an upper or lower notification
    const className = this.getYPosition(options) === 'top' ? 'upper' : 'lower'
    notificationElem.classList.add('notyf__toast--' + className)
    return notificationElem
  }
  NotyfView.prototype._createHTMLElement = function (_a) {
    const tagName = _a.tagName
    const className = _a.className
    const text = _a.text
    const elem = document.createElement(tagName)
    if (className) {
      elem.className = className
    }
    elem.textContent = text || null
    return elem
  }
  /**
   * Creates an invisible container which will announce the notyfs to
   * screen readers
   */
  NotyfView.prototype._createA11yContainer = function () {
    const a11yContainer = this._createHTMLElement({ tagName: 'div', className: 'notyf-announcer' })
    a11yContainer.setAttribute('aria-atomic', 'true')
    a11yContainer.setAttribute('aria-live', 'polite')
    // Set the a11y container to be visible hidden. Can't use display: none as
    // screen readers won't read it.
    a11yContainer.style.border = '0'
    a11yContainer.style.clip = 'rect(0 0 0 0)'
    a11yContainer.style.height = '1px'
    a11yContainer.style.margin = '-1px'
    a11yContainer.style.overflow = 'hidden'
    a11yContainer.style.padding = '0'
    a11yContainer.style.position = 'absolute'
    a11yContainer.style.width = '1px'
    a11yContainer.style.outline = '0'
    document.body.appendChild(a11yContainer)
    this.a11yContainer = a11yContainer
  }
  /**
   * Announces a message to screenreaders.
   */
  NotyfView.prototype._announce = function (message) {
    const _this = this
    this.a11yContainer.textContent = ''
    // This 100ms timeout is necessary for some browser + screen-reader combinations:
    // - Both JAWS and NVDA over IE11 will not announce anything without a non-zero timeout.
    // - With Chrome and IE11 with NVDA or JAWS, a repeated (identical) message won't be read a
    //   second time without clearing and then using a non-zero delay.
    // (using JAWS 17 at time of this writing).
    // https://github.com/angular/material2/blob/master/src/cdk/a11y/live-announcer/live-announcer.ts
    setTimeout(function () {
      _this.a11yContainer.textContent = message
    }, 100)
  }
  /**
   * Determine which animationend event is supported
   */
  NotyfView.prototype._getAnimationEndEventName = function () {
    const el = document.createElement('_fake')
    const transitions = {
      MozTransition: 'animationend',
      OTransition: 'oAnimationEnd',
      WebkitTransition: 'webkitAnimationEnd',
      transition: 'animationend'
    }
    let t
    for (t in transitions) {
      if (el.style[t] !== undefined) {
        return transitions[t]
      }
    }
    // No supported animation end event. Using "animationend" as a fallback
    return 'animationend'
  }
  return NotyfView
})()

/**
 * Main controller class. Defines the main Notyf API.
 */
const Notyf = /** @class */ (function () {
  function Notyf (opts) {
    const _this = this
    this.dismiss = this._removeNotification
    this.notifications = new NotyfArray()
    this.view = new NotyfView()
    const types = this.registerTypes(opts)
    this.options = __assign(__assign({}, DEFAULT_OPTIONS), opts)
    this.options.types = types
    this.notifications.onUpdate(function (elem, type) {
      return _this.view.update(elem, type)
    })
    this.view.on(NotyfEvent.Dismiss, function (_a) {
      const target = _a.target
      const event = _a.event
      _this._removeNotification(target)
      // tslint:disable-next-line: no-string-literal
      target.triggerEvent(NotyfEvent.Dismiss, event)
    })
    // tslint:disable-next-line: no-string-literal
    this.view.on(NotyfEvent.Click, function (_a) {
      const target = _a.target
      const event = _a.event
      return target.triggerEvent(NotyfEvent.Click, event)
    })
  }
  Notyf.prototype.error = function (payload) {
    const options = this.normalizeOptions('error', payload)
    return this.open(options)
  }
  Notyf.prototype.success = function (payload) {
    const options = this.normalizeOptions('success', payload)
    return this.open(options)
  }
  Notyf.prototype.open = function (options) {
    const defaultOpts =
      this.options.types.find(function (_a) {
        const type = _a.type
        return type === options.type
      }) || {}
    const config = __assign(__assign({}, defaultOpts), options)
    this.assignProps(['ripple', 'position', 'dismissible'], config)
    const notification = new NotyfNotification(config)
    this._pushNotification(notification)
    return notification
  }
  Notyf.prototype.dismissAll = function () {
    while (this.notifications.splice(0, 1));
  }
  /**
   * Assigns properties to a config object based on two rules:
   * 1. If the config object already sets that prop, leave it as so
   * 2. Otherwise, use the default prop from the global options
   *
   * It's intended to build the final config object to open a notification. e.g. if
   * 'dismissible' is not set, then use the value from the global config.
   *
   * @param props - properties to be assigned to the config object
   * @param config - object whose properties need to be set
   */
  Notyf.prototype.assignProps = function (props, config) {
    const _this = this
    props.forEach(function (prop) {
      // intentional double equality to check for both null and undefined
      config[prop] = config[prop] == null ? _this.options[prop] : config[prop]
    })
  }
  Notyf.prototype._pushNotification = function (notification) {
    const _this = this
    this.notifications.push(notification)
    const duration =
      notification.options.duration !== undefined ? notification.options.duration : this.options.duration
    if (duration) {
      setTimeout(function () {
        return _this._removeNotification(notification)
      }, duration)
    }
  }
  Notyf.prototype._removeNotification = function (notification) {
    const index = this.notifications.indexOf(notification)
    if (index !== -1) {
      this.notifications.splice(index, 1)
    }
  }
  Notyf.prototype.normalizeOptions = function (type, payload) {
    let options = { type: type }
    if (typeof payload === 'string') {
      options.message = payload
    } else if (typeof payload === 'object') {
      options = __assign(__assign({}, options), payload)
    }
    return options
  }
  Notyf.prototype.registerTypes = function (opts) {
    const incomingTypes = ((opts && opts.types) || []).slice()
    const finalDefaultTypes = DEFAULT_OPTIONS.types.map(function (defaultType) {
      // find if there's a default type within the user input's types, if so, it means the user
      // wants to change some of the default settings
      let userTypeIdx = -1
      incomingTypes.forEach(function (t, idx) {
        if (t.type === defaultType.type) {
          userTypeIdx = idx
        }
      })
      const userType = userTypeIdx !== -1 ? incomingTypes.splice(userTypeIdx, 1)[0] : {}
      return __assign(__assign({}, defaultType), userType)
    })
    return finalDefaultTypes.concat(incomingTypes)
  }
  return Notyf
})()

export { DEFAULT_OPTIONS, Notyf, NotyfArray, NotyfArrayEvent, NotyfEvent, NotyfNotification, NotyfView }
