parcelRequire = (function (e, r, t, n) { let i; const o = typeof parcelRequire === 'function' && parcelRequire; const u = typeof require === 'function' && require; function f (t, n) { if (!r[t]) { if (!e[t]) { const i = typeof parcelRequire === 'function' && parcelRequire; if (!n && i) return i(t, !0); if (o) return o(t, !0); if (u && typeof t === 'string') return u(t); const c = new Error("Cannot find module '" + t + "'"); throw c.code = 'MODULE_NOT_FOUND', c }p.resolve = function (r) { return e[t][1][r] || r }, p.cache = {}; const l = r[t] = new f.Module(t); e[t][0].call(l.exports, p, l, l.exports, this) } return r[t].exports; function p (e) { return f(p.resolve(e)) } }f.isParcelRequire = !0, f.Module = function (e) { this.id = e, this.bundle = f, this.exports = {} }, f.modules = e, f.cache = r, f.parent = o, f.register = function (r, t) { e[r] = [function (e, r) { r.exports = t }, {}] }; for (let c = 0; c < t.length; c++) try { f(t[c]) } catch (e) { i || (i = e) } if (t.length) { const l = f(t[t.length - 1]); typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = l : typeof define === 'function' && define.amd ? define(function () { return l }) : n && (this[n] = l) } if (parcelRequire = f, i) throw i; return f }({
  Omyb: [function (require, module, exports) {
    'use strict'; function e (e, t) { const r = window.MutationObserver; if (r) { const n = new r(t); return n.observe(e, { childList: !0, subtree: !0 }), n } return e.addEventListener('DOMNodeInserted', t, !1), e.addEventListener('DOMNodeRemoved', t, !1), null }Object.defineProperty(exports, '__esModule', { value: !0 }), exports.default = e
  }, {}],
  A8OV: [function (require, module, exports) {
    'use strict'; const e = this && this.__importDefault || function (e) { return e && e.__esModule ? e : { default: e } }; Object.defineProperty(exports, '__esModule', { value: !0 }); const t = e(require('../helpers/observe-dom')); function s () { const e = this; const s = this.options.container; s instanceof HTMLElement && (window.getComputedStyle(s).position === 'static' && (s.style.position = 'relative')); this._observer = t.default(document.querySelector('body'), function () { Object.keys(e.trackedElements).forEach(function (t) { e.on('enter', t), e.on('leave', t) }) }), s.addEventListener('scroll', this._scroll, { passive: !0 }), window.addEventListener('resize', this._scroll, { passive: !0 }), this._scroll(), this.attached = !0 }exports.default = s
  }, { '../helpers/observe-dom': 'Omyb' }],
  OJn0: [function (require, module, exports) {
    'use strict'; function e (e, t) { if (!e) throw new Error('You should specify the element you want to test'); typeof e === 'string' && (e = document.querySelector(e)); const n = e.getBoundingClientRect(); return n.bottom - t.tolerance > 0 && n.right - t.tolerance > 0 && n.left + t.tolerance < (window.innerWidth || document.documentElement.clientWidth) && n.top + t.tolerance < (window.innerHeight || document.documentElement.clientHeight) }Object.defineProperty(exports, '__esModule', { value: !0 }), exports.default = e
  }, {}],
  m6QN: [function (require, module, exports) {
    'use strict'; function e (e, t) { if (!e) throw new Error('You should specify the element you want to test'); if (typeof e === 'string' && (e = document.querySelector(e)), typeof t === 'string' && (t = { tolerance: 0, container: document.querySelector(t) }), typeof t.container === 'string' && (t.container = document.querySelector(t.container)), t instanceof HTMLElement && (t = { tolerance: 0, container: t }), !t.container) throw new Error('You should specify a container element'); const o = t.container.getBoundingClientRect(); return e.offsetTop + e.clientHeight - t.tolerance > t.container.scrollTop && e.offsetLeft + e.clientWidth - t.tolerance > t.container.scrollLeft && e.offsetLeft + t.tolerance < o.width + t.container.scrollLeft && e.offsetTop + t.tolerance < o.height + t.container.scrollTop }Object.defineProperty(exports, '__esModule', { value: !0 }), exports.default = e
  }, {}],
  VqMh: [function (require, module, exports) {
    'use strict'; const e = this && this.__importDefault || function (e) { return e && e.__esModule ? e : { default: e } }; Object.defineProperty(exports, '__esModule', { value: !0 }); const i = e(require('./in-viewport')); const n = e(require('./in-container')); function t (e, t) { void 0 === e && (e = {}), void 0 === t && (t = { container: window, tolerance: 0 }); let o; const r = Object.keys(e); r.length && (o = t.container === window ? i.default : n.default, r.forEach(function (i) { e[i].nodes.forEach(function (n) { if (o(n.node, t) ? (n.wasVisible = n.isVisible, n.isVisible = !0) : (n.wasVisible = n.isVisible, n.isVisible = !1), !0 === n.isVisible && !1 === n.wasVisible) { if (!e[i].enter) return; Object.keys(e[i].enter).forEach(function (t) { typeof e[i].enter[t] === 'function' && e[i].enter[t](n.node, 'enter') }) } if (!1 === n.isVisible && !0 === n.wasVisible) { if (!e[i].leave) return; Object.keys(e[i].leave).forEach(function (t) { typeof e[i].leave[t] === 'function' && e[i].leave[t](n.node, 'leave') }) } }) })) }exports.default = t
  }, { './in-viewport': 'OJn0', './in-container': 'm6QN' }],
  GRp5: [function (require, module, exports) {
    'use strict'; const e = this && this.__importDefault || function (e) { return e && e.__esModule ? e : { default: e } }; Object.defineProperty(exports, '__esModule', { value: !0 }); const t = e(require('../helpers/scroll-handler')); function r () { let e; const r = this; return function () { clearTimeout(e), e = setTimeout(function () { t.default(r.trackedElements, r.options) }, r.options.debounce) } }exports.default = r
  }, { '../helpers/scroll-handler': 'VqMh' }],
  FO0g: [function (require, module, exports) {
    'use strict'; function e () { this._observer instanceof MutationObserver && this._observer.disconnect(), this.options.container.removeEventListener('scroll', this._scroll), window.removeEventListener('resize', this._scroll), this.attached = !1 }Object.defineProperty(exports, '__esModule', { value: !0 }), exports.default = e
  }, {}],
  nGOL: [function (require, module, exports) {
    'use strict'; function e (e, t, s) { const l = Object.keys(this.trackedElements[t].enter || {}); const n = Object.keys(this.trackedElements[t].leave || {}); if ({}.hasOwnProperty.call(this.trackedElements, t)) if (s) { if (this.trackedElements[t][e]) { const r = typeof s === 'function' ? s.name : s; delete this.trackedElements[t][e][r] } } else delete this.trackedElements[t][e]; l.length || n.length || delete this.trackedElements[t] }Object.defineProperty(exports, '__esModule', { value: !0 }), exports.default = e
  }, {}],
  NKIH: [function (require, module, exports) {
    'use strict'; function e (e, t, r) { if (!e) throw new Error('No event given. Choose either enter or leave'); if (!t) throw new Error('No selector to track'); if (['enter', 'leave'].indexOf(e) < 0) throw new Error(e + ' event is not supported'); ({}).hasOwnProperty.call(this.trackedElements, t) || (this.trackedElements[t] = {}), this.trackedElements[t].nodes = []; for (let s = 0, n = document.querySelectorAll(t); s < n.length; s++) { const o = { isVisible: !1, wasVisible: !1, node: n[s] }; this.trackedElements[t].nodes.push(o) } typeof r === 'function' && (this.trackedElements[t][e] || (this.trackedElements[t][e] = {}), this.trackedElements[t][e][r.name || 'anonymous'] = r) }Object.defineProperty(exports, '__esModule', { value: !0 }), exports.default = e
  }, {}],
  QCba: [function (require, module, exports) {
    'use strict'; const e = this && this.__importDefault || function (e) { return e && e.__esModule ? e : { default: e } }; Object.defineProperty(exports, '__esModule', { value: !0 }); const t = e(require('./methods/attach')); const r = e(require('./methods/debounced-scroll')); const n = e(require('./methods/destroy')); const o = e(require('./methods/off')); const i = e(require('./methods/on')); const u = e(require('./helpers/in-viewport')); function a (e) { void 0 === e && (e = { tolerance: 0, debounce: 100, container: window }), this.options = {}, this.trackedElements = {}, Object.defineProperties(this.options, { container: { configurable: !1, enumerable: !1, get: function () { let t; return typeof e.container === 'string' ? t = document.querySelector(e.container) : e.container instanceof HTMLElement && (t = e.container), t || window }, set: function (t) { e.container = t } }, debounce: { get: function () { return e.debounce || 100 }, set: function (t) { e.debounce = t } }, tolerance: { get: function () { return e.tolerance || 0 }, set: function (t) { e.tolerance = t } } }), Object.defineProperty(this, '_scroll', { enumerable: !1, configurable: !1, writable: !1, value: this._debouncedScroll.call(this) }), this.attach() }Object.defineProperties(a.prototype, { _debouncedScroll: { configurable: !1, writable: !1, enumerable: !1, value: r.default }, attach: { configurable: !1, writable: !1, enumerable: !1, value: t.default }, destroy: { configurable: !1, writable: !1, enumerable: !1, value: n.default }, off: { configurable: !1, writable: !1, enumerable: !1, value: o.default }, on: { configurable: !1, writable: !1, enumerable: !1, value: i.default } }), a.check = u.default, exports.default = a
  }, { './methods/attach': 'A8OV', './methods/debounced-scroll': 'GRp5', './methods/destroy': 'FO0g', './methods/off': 'nGOL', './methods/on': 'NKIH', './helpers/in-viewport': 'OJn0' }]
}, {}, ['QCba'], null))
