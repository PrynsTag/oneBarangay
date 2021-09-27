(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('jquery'))
    : typeof define === 'function' && define.amd ? define(['jquery'], factory)
      : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.jQuery))
}(this, function ($) {
  'use strict'

  function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { default: e } }

  const $__default = /* #__PURE__ */_interopDefaultLegacy($)

  function _classCallCheck (instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError('Cannot call a class as a function')
    }
  }

  function _defineProperties (target, props) {
    for (let i = 0; i < props.length; i++) {
      const descriptor = props[i]
      descriptor.enumerable = descriptor.enumerable || false
      descriptor.configurable = true
      if ('value' in descriptor) descriptor.writable = true
      Object.defineProperty(target, descriptor.key, descriptor)
    }
  }

  function _createClass (Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps)
    if (staticProps) _defineProperties(Constructor, staticProps)
    return Constructor
  }

  function _inherits (subClass, superClass) {
    if (typeof superClass !== 'function' && superClass !== null) {
      throw new TypeError('Super expression must either be null or a function')
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        writable: true,
        configurable: true
      }
    })
    if (superClass) _setPrototypeOf(subClass, superClass)
  }

  function _getPrototypeOf (o) {
    _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf (o) {
      return o.__proto__ || Object.getPrototypeOf(o)
    }
    return _getPrototypeOf(o)
  }

  function _setPrototypeOf (o, p) {
    _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf (o, p) {
      o.__proto__ = p
      return o
    }

    return _setPrototypeOf(o, p)
  }

  function _isNativeReflectConstruct () {
    if (typeof Reflect === 'undefined' || !Reflect.construct) return false
    if (Reflect.construct.sham) return false
    if (typeof Proxy === 'function') return true

    try {
      Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {}))
      return true
    } catch (e) {
      return false
    }
  }

  function _assertThisInitialized (self) {
    if (self === void 0) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called")
    }

    return self
  }

  function _possibleConstructorReturn (self, call) {
    if (call && (typeof call === 'object' || typeof call === 'function')) {
      return call
    }

    return _assertThisInitialized(self)
  }

  function _createSuper (Derived) {
    const hasNativeReflectConstruct = _isNativeReflectConstruct()

    return function _createSuperInternal () {
      const Super = _getPrototypeOf(Derived)
      let result

      if (hasNativeReflectConstruct) {
        const NewTarget = _getPrototypeOf(this).constructor

        result = Reflect.construct(Super, arguments, NewTarget)
      } else {
        result = Super.apply(this, arguments)
      }

      return _possibleConstructorReturn(this, result)
    }
  }

  function _superPropBase (object, property) {
    while (!Object.prototype.hasOwnProperty.call(object, property)) {
      object = _getPrototypeOf(object)
      if (object === null) break
    }

    return object
  }

  function _get (target, property, receiver) {
    if (typeof Reflect !== 'undefined' && Reflect.get) {
      _get = Reflect.get
    } else {
      _get = function _get (target, property, receiver) {
        const base = _superPropBase(target, property)

        if (!base) return
        const desc = Object.getOwnPropertyDescriptor(base, property)

        if (desc.get) {
          return desc.get.call(receiver)
        }

        return desc.value
      }
    }

    return _get(target, property, receiver || target)
  }

  function _slicedToArray (arr, i) {
    return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest()
  }

  function _arrayWithHoles (arr) {
    if (Array.isArray(arr)) return arr
  }

  function _iterableToArrayLimit (arr, i) {
    if (typeof Symbol === 'undefined' || !(Symbol.iterator in Object(arr))) return
    const _arr = []
    let _n = true
    let _d = false
    let _e

    try {
      for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
        _arr.push(_s.value)

        if (i && _arr.length === i) break
      }
    } catch (err) {
      _d = true
      _e = err
    } finally {
      try {
        if (!_n && _i.return != null) _i.return()
      } finally {
        if (_d) throw _e
      }
    }

    return _arr
  }

  function _unsupportedIterableToArray (o, minLen) {
    if (!o) return
    if (typeof o === 'string') return _arrayLikeToArray(o, minLen)
    let n = Object.prototype.toString.call(o).slice(8, -1)
    if (n === 'Object' && o.constructor) n = o.constructor.name
    if (n === 'Map' || n === 'Set') return Array.from(o)
    if (n === 'Arguments' || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen)
  }

  function _arrayLikeToArray (arr, len) {
    if (len == null || len > arr.length) len = arr.length

    for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]

    return arr2
  }

  function _nonIterableRest () {
    throw new TypeError('Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.')
  }

  const commonjsGlobal = typeof globalThis !== 'undefined' ? globalThis : typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : typeof self !== 'undefined' ? self : {}

  function createCommonjsModule (fn, module) {
  	return module = { exports: {} }, fn(module, module.exports), module.exports
  }

  const check = function (it) {
    return it && it.Math == Math && it
  }

  // https://github.com/zloirock/core-js/issues/86#issuecomment-115759028
  const global_1 =
    /* global globalThis -- safe */
    check(typeof globalThis === 'object' && globalThis) ||
    check(typeof window === 'object' && window) ||
    check(typeof self === 'object' && self) ||
    check(typeof commonjsGlobal === 'object' && commonjsGlobal) ||
    // eslint-disable-next-line no-new-func -- fallback
    (function () { return this })() || Function('return this')()

  const fails = function (exec) {
    try {
      return !!exec()
    } catch (error) {
      return true
    }
  }

  // Detect IE8's incomplete defineProperty implementation
  const descriptors = !fails(function () {
    return Object.defineProperty({}, 1, { get: function () { return 7 } })[1] != 7
  })

  const nativePropertyIsEnumerable = {}.propertyIsEnumerable
  const getOwnPropertyDescriptor$1 = Object.getOwnPropertyDescriptor

  // Nashorn ~ JDK8 bug
  const NASHORN_BUG = getOwnPropertyDescriptor$1 && !nativePropertyIsEnumerable.call({ 1: 2 }, 1)

  // `Object.prototype.propertyIsEnumerable` method implementation
  // https://tc39.es/ecma262/#sec-object.prototype.propertyisenumerable
  const f$4 = NASHORN_BUG ? function propertyIsEnumerable (V) {
    const descriptor = getOwnPropertyDescriptor$1(this, V)
    return !!descriptor && descriptor.enumerable
  } : nativePropertyIsEnumerable

  const objectPropertyIsEnumerable = {
  	f: f$4
  }

  const createPropertyDescriptor = function (bitmap, value) {
    return {
      enumerable: !(bitmap & 1),
      configurable: !(bitmap & 2),
      writable: !(bitmap & 4),
      value: value
    }
  }

  const toString = {}.toString

  const classofRaw = function (it) {
    return toString.call(it).slice(8, -1)
  }

  const split = ''.split

  // fallback for non-array-like ES3 and non-enumerable old V8 strings
  const indexedObject = fails(function () {
    // throws an error in rhino, see https://github.com/mozilla/rhino/issues/346
    // eslint-disable-next-line no-prototype-builtins -- safe
    return !Object('z').propertyIsEnumerable(0)
  }) ? function (it) {
        return classofRaw(it) == 'String' ? split.call(it, '') : Object(it)
      } : Object

  // `RequireObjectCoercible` abstract operation
  // https://tc39.es/ecma262/#sec-requireobjectcoercible
  const requireObjectCoercible = function (it) {
    if (it == undefined) throw TypeError("Can't call method on " + it)
    return it
  }

  // toObject with fallback for non-array-like ES3 strings

  const toIndexedObject = function (it) {
    return indexedObject(requireObjectCoercible(it))
  }

  const isObject = function (it) {
    return typeof it === 'object' ? it !== null : typeof it === 'function'
  }

  // `ToPrimitive` abstract operation
  // https://tc39.es/ecma262/#sec-toprimitive
  // instead of the ES6 spec version, we didn't implement @@toPrimitive case
  // and the second argument - flag - preferred type is a string
  const toPrimitive = function (input, PREFERRED_STRING) {
    if (!isObject(input)) return input
    let fn, val
    if (PREFERRED_STRING && typeof (fn = input.toString) === 'function' && !isObject(val = fn.call(input))) return val
    if (typeof (fn = input.valueOf) === 'function' && !isObject(val = fn.call(input))) return val
    if (!PREFERRED_STRING && typeof (fn = input.toString) === 'function' && !isObject(val = fn.call(input))) return val
    throw TypeError("Can't convert object to primitive value")
  }

  const hasOwnProperty = {}.hasOwnProperty

  const has$1 = function (it, key) {
    return hasOwnProperty.call(it, key)
  }

  const document$1 = global_1.document
  // typeof document.createElement is 'object' in old IE
  const EXISTS = isObject(document$1) && isObject(document$1.createElement)

  const documentCreateElement = function (it) {
    return EXISTS ? document$1.createElement(it) : {}
  }

  // Thank's IE8 for his funny defineProperty
  const ie8DomDefine = !descriptors && !fails(function () {
    return Object.defineProperty(documentCreateElement('div'), 'a', {
      get: function () { return 7 }
    }).a != 7
  })

  const nativeGetOwnPropertyDescriptor = Object.getOwnPropertyDescriptor

  // `Object.getOwnPropertyDescriptor` method
  // https://tc39.es/ecma262/#sec-object.getownpropertydescriptor
  const f$3 = descriptors ? nativeGetOwnPropertyDescriptor : function getOwnPropertyDescriptor (O, P) {
    O = toIndexedObject(O)
    P = toPrimitive(P, true)
    if (ie8DomDefine) {
      try {
        return nativeGetOwnPropertyDescriptor(O, P)
      } catch (error) { /* empty */ }
    }
    if (has$1(O, P)) return createPropertyDescriptor(!objectPropertyIsEnumerable.f.call(O, P), O[P])
  }

  const objectGetOwnPropertyDescriptor = {
  	f: f$3
  }

  const anObject = function (it) {
    if (!isObject(it)) {
      throw TypeError(String(it) + ' is not an object')
    } return it
  }

  const nativeDefineProperty = Object.defineProperty

  // `Object.defineProperty` method
  // https://tc39.es/ecma262/#sec-object.defineproperty
  const f$2 = descriptors ? nativeDefineProperty : function defineProperty (O, P, Attributes) {
    anObject(O)
    P = toPrimitive(P, true)
    anObject(Attributes)
    if (ie8DomDefine) {
      try {
        return nativeDefineProperty(O, P, Attributes)
      } catch (error) { /* empty */ }
    }
    if ('get' in Attributes || 'set' in Attributes) throw TypeError('Accessors not supported')
    if ('value' in Attributes) O[P] = Attributes.value
    return O
  }

  const objectDefineProperty = {
  	f: f$2
  }

  const createNonEnumerableProperty = descriptors ? function (object, key, value) {
    return objectDefineProperty.f(object, key, createPropertyDescriptor(1, value))
  } : function (object, key, value) {
    object[key] = value
    return object
  }

  const setGlobal = function (key, value) {
    try {
      createNonEnumerableProperty(global_1, key, value)
    } catch (error) {
      global_1[key] = value
    } return value
  }

  const SHARED = '__core-js_shared__'
  const store$1 = global_1[SHARED] || setGlobal(SHARED, {})

  const sharedStore = store$1

  const functionToString = Function.toString

  // this helper broken in `3.4.1-3.4.4`, so we can't use `shared` helper
  if (typeof sharedStore.inspectSource !== 'function') {
    sharedStore.inspectSource = function (it) {
      return functionToString.call(it)
    }
  }

  const inspectSource = sharedStore.inspectSource

  const WeakMap$1 = global_1.WeakMap

  const nativeWeakMap = typeof WeakMap$1 === 'function' && /native code/.test(inspectSource(WeakMap$1))

  const shared = createCommonjsModule(function (module) {
    (module.exports = function (key, value) {
      return sharedStore[key] || (sharedStore[key] = value !== undefined ? value : {})
    })('versions', []).push({
      version: '3.9.1',
      mode: 'global',
      copyright: '© 2021 Denis Pushkarev (zloirock.ru)'
    })
  })

  let id = 0
  const postfix = Math.random()

  const uid = function (key) {
    return 'Symbol(' + String(key === undefined ? '' : key) + ')_' + (++id + postfix).toString(36)
  }

  const keys = shared('keys')

  const sharedKey = function (key) {
    return keys[key] || (keys[key] = uid(key))
  }

  const hiddenKeys$1 = {}

  const WeakMap = global_1.WeakMap
  let set, get, has

  const enforce = function (it) {
    return has(it) ? get(it) : set(it, {})
  }

  const getterFor = function (TYPE) {
    return function (it) {
      let state
      if (!isObject(it) || (state = get(it)).type !== TYPE) {
        throw TypeError('Incompatible receiver, ' + TYPE + ' required')
      } return state
    }
  }

  if (nativeWeakMap) {
    const store = sharedStore.state || (sharedStore.state = new WeakMap())
    const wmget = store.get
    const wmhas = store.has
    const wmset = store.set
    set = function (it, metadata) {
      metadata.facade = it
      wmset.call(store, it, metadata)
      return metadata
    }
    get = function (it) {
      return wmget.call(store, it) || {}
    }
    has = function (it) {
      return wmhas.call(store, it)
    }
  } else {
    const STATE = sharedKey('state')
    hiddenKeys$1[STATE] = true
    set = function (it, metadata) {
      metadata.facade = it
      createNonEnumerableProperty(it, STATE, metadata)
      return metadata
    }
    get = function (it) {
      return has$1(it, STATE) ? it[STATE] : {}
    }
    has = function (it) {
      return has$1(it, STATE)
    }
  }

  const internalState = {
    set: set,
    get: get,
    has: has,
    enforce: enforce,
    getterFor: getterFor
  }

  const redefine = createCommonjsModule(function (module) {
    const getInternalState = internalState.get
    const enforceInternalState = internalState.enforce
    const TEMPLATE = String(String).split('String');

    (module.exports = function (O, key, value, options) {
      const unsafe = options ? !!options.unsafe : false
      let simple = options ? !!options.enumerable : false
      const noTargetGet = options ? !!options.noTargetGet : false
      let state
      if (typeof value === 'function') {
        if (typeof key === 'string' && !has$1(value, 'name')) {
          createNonEnumerableProperty(value, 'name', key)
        }
        state = enforceInternalState(value)
        if (!state.source) {
          state.source = TEMPLATE.join(typeof key === 'string' ? key : '')
        }
      }
      if (O === global_1) {
        if (simple) O[key] = value
        else setGlobal(key, value)
        return
      } else if (!unsafe) {
        delete O[key]
      } else if (!noTargetGet && O[key]) {
        simple = true
      }
      if (simple) O[key] = value
      else createNonEnumerableProperty(O, key, value)
      // add fake Function#toString for correct work wrapped methods / constructors with methods like LoDash isNative
    })(Function.prototype, 'toString', function toString () {
      return typeof this === 'function' && getInternalState(this).source || inspectSource(this)
    })
  })

  const path = global_1

  const aFunction$1 = function (variable) {
    return typeof variable === 'function' ? variable : undefined
  }

  const getBuiltIn = function (namespace, method) {
    return arguments.length < 2 ? aFunction$1(path[namespace]) || aFunction$1(global_1[namespace])
      : path[namespace] && path[namespace][method] || global_1[namespace] && global_1[namespace][method]
  }

  const ceil = Math.ceil
  const floor = Math.floor

  // `ToInteger` abstract operation
  // https://tc39.es/ecma262/#sec-tointeger
  const toInteger = function (argument) {
    return isNaN(argument = +argument) ? 0 : (argument > 0 ? floor : ceil)(argument)
  }

  const min$1 = Math.min

  // `ToLength` abstract operation
  // https://tc39.es/ecma262/#sec-tolength
  const toLength = function (argument) {
    return argument > 0 ? min$1(toInteger(argument), 0x1FFFFFFFFFFFFF) : 0 // 2 ** 53 - 1 == 9007199254740991
  }

  const max = Math.max
  const min = Math.min

  // Helper for a popular repeating case of the spec:
  // Let integer be ? ToInteger(index).
  // If integer < 0, let result be max((length + integer), 0); else let result be min(integer, length).
  const toAbsoluteIndex = function (index, length) {
    const integer = toInteger(index)
    return integer < 0 ? max(integer + length, 0) : min(integer, length)
  }

  // `Array.prototype.{ indexOf, includes }` methods implementation
  const createMethod$3 = function (IS_INCLUDES) {
    return function ($this, el, fromIndex) {
      const O = toIndexedObject($this)
      const length = toLength(O.length)
      let index = toAbsoluteIndex(fromIndex, length)
      let value
      // Array#includes uses SameValueZero equality algorithm
      // eslint-disable-next-line no-self-compare -- NaN check
      if (IS_INCLUDES && el != el) {
        while (length > index) {
          value = O[index++]
          // eslint-disable-next-line no-self-compare -- NaN check
          if (value != value) return true
          // Array#indexOf ignores holes, Array#includes - not
        }
      } else {
        for (;length > index; index++) {
          if ((IS_INCLUDES || index in O) && O[index] === el) return IS_INCLUDES || index || 0
        }
      } return !IS_INCLUDES && -1
    }
  }

  const arrayIncludes = {
    // `Array.prototype.includes` method
    // https://tc39.es/ecma262/#sec-array.prototype.includes
    includes: createMethod$3(true),
    // `Array.prototype.indexOf` method
    // https://tc39.es/ecma262/#sec-array.prototype.indexof
    indexOf: createMethod$3(false)
  }

  const indexOf = arrayIncludes.indexOf

  const objectKeysInternal = function (object, names) {
    const O = toIndexedObject(object)
    let i = 0
    const result = []
    let key
    for (key in O) !has$1(hiddenKeys$1, key) && has$1(O, key) && result.push(key)
    // Don't enum bug & hidden keys
    while (names.length > i) {
      if (has$1(O, key = names[i++])) {
        ~indexOf(result, key) || result.push(key)
      }
    }
    return result
  }

  // IE8- don't enum bug keys
  const enumBugKeys = [
    'constructor',
    'hasOwnProperty',
    'isPrototypeOf',
    'propertyIsEnumerable',
    'toLocaleString',
    'toString',
    'valueOf'
  ]

  const hiddenKeys = enumBugKeys.concat('length', 'prototype')

  // `Object.getOwnPropertyNames` method
  // https://tc39.es/ecma262/#sec-object.getownpropertynames
  const f$1 = Object.getOwnPropertyNames || function getOwnPropertyNames (O) {
    return objectKeysInternal(O, hiddenKeys)
  }

  const objectGetOwnPropertyNames = {
  	f: f$1
  }

  const f = Object.getOwnPropertySymbols

  const objectGetOwnPropertySymbols = {
  	f: f
  }

  // all object keys, includes non-enumerable and symbols
  const ownKeys = getBuiltIn('Reflect', 'ownKeys') || function ownKeys (it) {
    const keys = objectGetOwnPropertyNames.f(anObject(it))
    const getOwnPropertySymbols = objectGetOwnPropertySymbols.f
    return getOwnPropertySymbols ? keys.concat(getOwnPropertySymbols(it)) : keys
  }

  const copyConstructorProperties = function (target, source) {
    const keys = ownKeys(source)
    const defineProperty = objectDefineProperty.f
    const getOwnPropertyDescriptor = objectGetOwnPropertyDescriptor.f
    for (let i = 0; i < keys.length; i++) {
      const key = keys[i]
      if (!has$1(target, key)) defineProperty(target, key, getOwnPropertyDescriptor(source, key))
    }
  }

  const replacement = /#|\.prototype\./

  const isForced = function (feature, detection) {
    const value = data[normalize(feature)]
    return value == POLYFILL ? true
      : value == NATIVE ? false
        : typeof detection === 'function' ? fails(detection)
          : !!detection
  }

  var normalize = isForced.normalize = function (string) {
    return String(string).replace(replacement, '.').toLowerCase()
  }

  var data = isForced.data = {}
  var NATIVE = isForced.NATIVE = 'N'
  var POLYFILL = isForced.POLYFILL = 'P'

  const isForced_1 = isForced

  const getOwnPropertyDescriptor = objectGetOwnPropertyDescriptor.f

  /*
    options.target      - name of the target object
    options.global      - target is the global object
    options.stat        - export as static methods of target
    options.proto       - export as prototype methods of target
    options.real        - real prototype method for the `pure` version
    options.forced      - export even if the native feature is available
    options.bind        - bind methods to the target, required for the `pure` version
    options.wrap        - wrap constructors to preventing global pollution, required for the `pure` version
    options.unsafe      - use the simple assignment of property instead of delete + defineProperty
    options.sham        - add a flag to not completely full polyfills
    options.enumerable  - export as enumerable property
    options.noTargetGet - prevent calling a getter on target
  */
  const _export = function (options, source) {
    const TARGET = options.target
    const GLOBAL = options.global
    const STATIC = options.stat
    let FORCED, target, key, targetProperty, sourceProperty, descriptor
    if (GLOBAL) {
      target = global_1
    } else if (STATIC) {
      target = global_1[TARGET] || setGlobal(TARGET, {})
    } else {
      target = (global_1[TARGET] || {}).prototype
    }
    if (target) {
      for (key in source) {
        sourceProperty = source[key]
        if (options.noTargetGet) {
          descriptor = getOwnPropertyDescriptor(target, key)
          targetProperty = descriptor && descriptor.value
        } else targetProperty = target[key]
        FORCED = isForced_1(GLOBAL ? key : TARGET + (STATIC ? '.' : '#') + key, options.forced)
        // contained in target
        if (!FORCED && targetProperty !== undefined) {
          if (typeof sourceProperty === typeof targetProperty) continue
          copyConstructorProperties(sourceProperty, targetProperty)
        }
        // add a flag to not completely full polyfills
        if (options.sham || (targetProperty && targetProperty.sham)) {
          createNonEnumerableProperty(sourceProperty, 'sham', true)
        }
        // extend global
        redefine(target, key, sourceProperty, options)
      }
    }
  }

  // `Object.keys` method
  // https://tc39.es/ecma262/#sec-object.keys
  const objectKeys = Object.keys || function keys (O) {
    return objectKeysInternal(O, enumBugKeys)
  }

  const propertyIsEnumerable = objectPropertyIsEnumerable.f

  // `Object.{ entries, values }` methods implementation
  const createMethod$2 = function (TO_ENTRIES) {
    return function (it) {
      const O = toIndexedObject(it)
      const keys = objectKeys(O)
      const length = keys.length
      let i = 0
      const result = []
      let key
      while (length > i) {
        key = keys[i++]
        if (!descriptors || propertyIsEnumerable.call(O, key)) {
          result.push(TO_ENTRIES ? [key, O[key]] : O[key])
        }
      }
      return result
    }
  }

  const objectToArray = {
    // `Object.entries` method
    // https://tc39.es/ecma262/#sec-object.entries
    entries: createMethod$2(true),
    // `Object.values` method
    // https://tc39.es/ecma262/#sec-object.values
    values: createMethod$2(false)
  }

  const $entries = objectToArray.entries

  // `Object.entries` method
  // https://tc39.es/ecma262/#sec-object.entries
  _export({ target: 'Object', stat: true }, {
    entries: function entries (O) {
      return $entries(O)
    }
  })

  const aFunction = function (it) {
    if (typeof it !== 'function') {
      throw TypeError(String(it) + ' is not a function')
    } return it
  }

  // optional / simple context binding
  const functionBindContext = function (fn, that, length) {
    aFunction(fn)
    if (that === undefined) return fn
    switch (length) {
      case 0: return function () {
        return fn.call(that)
      }
      case 1: return function (a) {
        return fn.call(that, a)
      }
      case 2: return function (a, b) {
        return fn.call(that, a, b)
      }
      case 3: return function (a, b, c) {
        return fn.call(that, a, b, c)
      }
    }
    return function (/* ...args */) {
      return fn.apply(that, arguments)
    }
  }

  // `ToObject` abstract operation
  // https://tc39.es/ecma262/#sec-toobject
  const toObject = function (argument) {
    return Object(requireObjectCoercible(argument))
  }

  // `IsArray` abstract operation
  // https://tc39.es/ecma262/#sec-isarray
  const isArray = Array.isArray || function isArray (arg) {
    return classofRaw(arg) == 'Array'
  }

  const engineIsNode = classofRaw(global_1.process) == 'process'

  const engineUserAgent = getBuiltIn('navigator', 'userAgent') || ''

  const process = global_1.process
  const versions = process && process.versions
  const v8 = versions && versions.v8
  let match, version

  if (v8) {
    match = v8.split('.')
    version = match[0] + match[1]
  } else if (engineUserAgent) {
    match = engineUserAgent.match(/Edge\/(\d+)/)
    if (!match || match[1] >= 74) {
      match = engineUserAgent.match(/Chrome\/(\d+)/)
      if (match) version = match[1]
    }
  }

  const engineV8Version = version && +version

  const nativeSymbol = !!Object.getOwnPropertySymbols && !fails(function () {
    /* global Symbol -- required for testing */
    return !Symbol.sham &&
      // Chrome 38 Symbol has incorrect toString conversion
      // Chrome 38-40 symbols are not inherited from DOM collections prototypes to instances
      (engineIsNode ? engineV8Version === 38 : engineV8Version > 37 && engineV8Version < 41)
  })

  const useSymbolAsUid = nativeSymbol &&
    /* global Symbol -- safe */
    !Symbol.sham &&
    typeof Symbol.iterator === 'symbol'

  const WellKnownSymbolsStore = shared('wks')
  const Symbol$1 = global_1.Symbol
  const createWellKnownSymbol = useSymbolAsUid ? Symbol$1 : Symbol$1 && Symbol$1.withoutSetter || uid

  const wellKnownSymbol = function (name) {
    if (!has$1(WellKnownSymbolsStore, name) || !(nativeSymbol || typeof WellKnownSymbolsStore[name] === 'string')) {
      if (nativeSymbol && has$1(Symbol$1, name)) {
        WellKnownSymbolsStore[name] = Symbol$1[name]
      } else {
        WellKnownSymbolsStore[name] = createWellKnownSymbol('Symbol.' + name)
      }
    } return WellKnownSymbolsStore[name]
  }

  const SPECIES$1 = wellKnownSymbol('species')

  // `ArraySpeciesCreate` abstract operation
  // https://tc39.es/ecma262/#sec-arrayspeciescreate
  const arraySpeciesCreate = function (originalArray, length) {
    let C
    if (isArray(originalArray)) {
      C = originalArray.constructor
      // cross-realm fallback
      if (typeof C === 'function' && (C === Array || isArray(C.prototype))) C = undefined
      else if (isObject(C)) {
        C = C[SPECIES$1]
        if (C === null) C = undefined
      }
    } return new (C === undefined ? Array : C)(length === 0 ? 0 : length)
  }

  const push = [].push

  // `Array.prototype.{ forEach, map, filter, some, every, find, findIndex, filterOut }` methods implementation
  const createMethod$1 = function (TYPE) {
    const IS_MAP = TYPE == 1
    const IS_FILTER = TYPE == 2
    const IS_SOME = TYPE == 3
    const IS_EVERY = TYPE == 4
    const IS_FIND_INDEX = TYPE == 6
    const IS_FILTER_OUT = TYPE == 7
    const NO_HOLES = TYPE == 5 || IS_FIND_INDEX
    return function ($this, callbackfn, that, specificCreate) {
      const O = toObject($this)
      const self = indexedObject(O)
      const boundFunction = functionBindContext(callbackfn, that, 3)
      const length = toLength(self.length)
      let index = 0
      const create = specificCreate || arraySpeciesCreate
      const target = IS_MAP ? create($this, length) : IS_FILTER || IS_FILTER_OUT ? create($this, 0) : undefined
      let value, result
      for (;length > index; index++) {
        if (NO_HOLES || index in self) {
          value = self[index]
          result = boundFunction(value, index, O)
          if (TYPE) {
            if (IS_MAP) target[index] = result // map
            else if (result) {
              switch (TYPE) {
                case 3: return true // some
                case 5: return value // find
                case 6: return index // findIndex
                case 2: push.call(target, value) // filter
              }
            } else {
              switch (TYPE) {
                case 4: return false // every
                case 7: push.call(target, value) // filterOut
              }
            }
          }
        }
      }
      return IS_FIND_INDEX ? -1 : IS_SOME || IS_EVERY ? IS_EVERY : target
    }
  }

  const arrayIteration = {
    // `Array.prototype.forEach` method
    // https://tc39.es/ecma262/#sec-array.prototype.foreach
    forEach: createMethod$1(0),
    // `Array.prototype.map` method
    // https://tc39.es/ecma262/#sec-array.prototype.map
    map: createMethod$1(1),
    // `Array.prototype.filter` method
    // https://tc39.es/ecma262/#sec-array.prototype.filter
    filter: createMethod$1(2),
    // `Array.prototype.some` method
    // https://tc39.es/ecma262/#sec-array.prototype.some
    some: createMethod$1(3),
    // `Array.prototype.every` method
    // https://tc39.es/ecma262/#sec-array.prototype.every
    every: createMethod$1(4),
    // `Array.prototype.find` method
    // https://tc39.es/ecma262/#sec-array.prototype.find
    find: createMethod$1(5),
    // `Array.prototype.findIndex` method
    // https://tc39.es/ecma262/#sec-array.prototype.findIndex
    findIndex: createMethod$1(6),
    // `Array.prototype.filterOut` method
    // https://github.com/tc39/proposal-array-filtering
    filterOut: createMethod$1(7)
  }

  // `Object.defineProperties` method
  // https://tc39.es/ecma262/#sec-object.defineproperties
  const objectDefineProperties = descriptors ? Object.defineProperties : function defineProperties (O, Properties) {
    anObject(O)
    const keys = objectKeys(Properties)
    const length = keys.length
    let index = 0
    let key
    while (length > index) objectDefineProperty.f(O, key = keys[index++], Properties[key])
    return O
  }

  const html = getBuiltIn('document', 'documentElement')

  const GT = '>'
  const LT = '<'
  const PROTOTYPE = 'prototype'
  const SCRIPT = 'script'
  const IE_PROTO = sharedKey('IE_PROTO')

  const EmptyConstructor = function () { /* empty */ }

  const scriptTag = function (content) {
    return LT + SCRIPT + GT + content + LT + '/' + SCRIPT + GT
  }

  // Create object with fake `null` prototype: use ActiveX Object with cleared prototype
  const NullProtoObjectViaActiveX = function (activeXDocument) {
    activeXDocument.write(scriptTag(''))
    activeXDocument.close()
    const temp = activeXDocument.parentWindow.Object
    activeXDocument = null // avoid memory leak
    return temp
  }

  // Create object with fake `null` prototype: use iframe Object with cleared prototype
  const NullProtoObjectViaIFrame = function () {
    // Thrash, waste and sodomy: IE GC bug
    const iframe = documentCreateElement('iframe')
    const JS = 'java' + SCRIPT + ':'
    let iframeDocument
    iframe.style.display = 'none'
    html.appendChild(iframe)
    // https://github.com/zloirock/core-js/issues/475
    iframe.src = String(JS)
    iframeDocument = iframe.contentWindow.document
    iframeDocument.open()
    iframeDocument.write(scriptTag('document.F=Object'))
    iframeDocument.close()
    return iframeDocument.F
  }

  // Check for document.domain and active x support
  // No need to use active x approach when document.domain is not set
  // see https://github.com/es-shims/es5-shim/issues/150
  // variation of https://github.com/kitcambridge/es5-shim/commit/4f738ac066346
  // avoid IE GC bug
  let activeXDocument
  var NullProtoObject = function () {
    try {
      /* global ActiveXObject -- old IE */
      activeXDocument = document.domain && new ActiveXObject('htmlfile')
    } catch (error) { /* ignore */ }
    NullProtoObject = activeXDocument ? NullProtoObjectViaActiveX(activeXDocument) : NullProtoObjectViaIFrame()
    let length = enumBugKeys.length
    while (length--) delete NullProtoObject[PROTOTYPE][enumBugKeys[length]]
    return NullProtoObject()
  }

  hiddenKeys$1[IE_PROTO] = true

  // `Object.create` method
  // https://tc39.es/ecma262/#sec-object.create
  const objectCreate = Object.create || function create (O, Properties) {
    let result
    if (O !== null) {
      EmptyConstructor[PROTOTYPE] = anObject(O)
      result = new EmptyConstructor()
      EmptyConstructor[PROTOTYPE] = null
      // add "__proto__" for Object.getPrototypeOf polyfill
      result[IE_PROTO] = O
    } else result = NullProtoObject()
    return Properties === undefined ? result : objectDefineProperties(result, Properties)
  }

  const UNSCOPABLES = wellKnownSymbol('unscopables')
  const ArrayPrototype = Array.prototype

  // Array.prototype[@@unscopables]
  // https://tc39.es/ecma262/#sec-array.prototype-@@unscopables
  if (ArrayPrototype[UNSCOPABLES] == undefined) {
    objectDefineProperty.f(ArrayPrototype, UNSCOPABLES, {
      configurable: true,
      value: objectCreate(null)
    })
  }

  // add a key to Array.prototype[@@unscopables]
  const addToUnscopables = function (key) {
    ArrayPrototype[UNSCOPABLES][key] = true
  }

  const $find = arrayIteration.find

  const FIND = 'find'
  let SKIPS_HOLES = true

  // Shouldn't skip holes
  if (FIND in []) Array(1)[FIND](function () { SKIPS_HOLES = false })

  // `Array.prototype.find` method
  // https://tc39.es/ecma262/#sec-array.prototype.find
  _export({ target: 'Array', proto: true, forced: SKIPS_HOLES }, {
    find: function find (callbackfn /* , that = undefined */) {
      return $find(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined)
    }
  })

  // https://tc39.es/ecma262/#sec-array.prototype-@@unscopables
  addToUnscopables(FIND)

  // a string of all valid unicode whitespaces
  const whitespaces = '\u0009\u000A\u000B\u000C\u000D\u0020\u00A0\u1680\u2000\u2001\u2002' +
    '\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u2028\u2029\uFEFF'

  const whitespace = '[' + whitespaces + ']'
  const ltrim = RegExp('^' + whitespace + whitespace + '*')
  const rtrim = RegExp(whitespace + whitespace + '*$')

  // `String.prototype.{ trim, trimStart, trimEnd, trimLeft, trimRight }` methods implementation
  const createMethod = function (TYPE) {
    return function ($this) {
      let string = String(requireObjectCoercible($this))
      if (TYPE & 1) string = string.replace(ltrim, '')
      if (TYPE & 2) string = string.replace(rtrim, '')
      return string
    }
  }

  const stringTrim = {
    // `String.prototype.{ trimLeft, trimStart }` methods
    // https://tc39.es/ecma262/#sec-string.prototype.trimstart
    start: createMethod(1),
    // `String.prototype.{ trimRight, trimEnd }` methods
    // https://tc39.es/ecma262/#sec-string.prototype.trimend
    end: createMethod(2),
    // `String.prototype.trim` method
    // https://tc39.es/ecma262/#sec-string.prototype.trim
    trim: createMethod(3)
  }

  const trim = stringTrim.trim

  const $parseInt = global_1.parseInt
  const hex = /^[+-]?0[Xx]/
  const FORCED$1 = $parseInt(whitespaces + '08') !== 8 || $parseInt(whitespaces + '0x16') !== 22

  // `parseInt` method
  // https://tc39.es/ecma262/#sec-parseint-string-radix
  const numberParseInt = FORCED$1 ? function parseInt (string, radix) {
    const S = trim(String(string))
    return $parseInt(S, (radix >>> 0) || (hex.test(S) ? 16 : 10))
  } : $parseInt

  // `parseInt` method
  // https://tc39.es/ecma262/#sec-parseint-string-radix
  _export({ global: true, forced: parseInt != numberParseInt }, {
    parseInt: numberParseInt
  })

  const SPECIES = wellKnownSymbol('species')

  const arrayMethodHasSpeciesSupport = function (METHOD_NAME) {
    // We can't use this feature detection in V8 since it causes
    // deoptimization and serious performance degradation
    // https://github.com/zloirock/core-js/issues/677
    return engineV8Version >= 51 || !fails(function () {
      const array = []
      const constructor = array.constructor = {}
      constructor[SPECIES] = function () {
        return { foo: 1 }
      }
      return array[METHOD_NAME](Boolean).foo !== 1
    })
  }

  const $filter = arrayIteration.filter

  const HAS_SPECIES_SUPPORT = arrayMethodHasSpeciesSupport('filter')

  // `Array.prototype.filter` method
  // https://tc39.es/ecma262/#sec-array.prototype.filter
  // with adding support of @@species
  _export({ target: 'Array', proto: true, forced: !HAS_SPECIES_SUPPORT }, {
    filter: function filter (callbackfn /* , thisArg */) {
      return $filter(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined)
    }
  })

  const createProperty = function (object, key, value) {
    const propertyKey = toPrimitive(key)
    if (propertyKey in object) objectDefineProperty.f(object, propertyKey, createPropertyDescriptor(0, value))
    else object[propertyKey] = value
  }

  const IS_CONCAT_SPREADABLE = wellKnownSymbol('isConcatSpreadable')
  const MAX_SAFE_INTEGER = 0x1FFFFFFFFFFFFF
  const MAXIMUM_ALLOWED_INDEX_EXCEEDED = 'Maximum allowed index exceeded'

  // We can't use this feature detection in V8 since it causes
  // deoptimization and serious performance degradation
  // https://github.com/zloirock/core-js/issues/679
  const IS_CONCAT_SPREADABLE_SUPPORT = engineV8Version >= 51 || !fails(function () {
    const array = []
    array[IS_CONCAT_SPREADABLE] = false
    return array.concat()[0] !== array
  })

  const SPECIES_SUPPORT = arrayMethodHasSpeciesSupport('concat')

  const isConcatSpreadable = function (O) {
    if (!isObject(O)) return false
    const spreadable = O[IS_CONCAT_SPREADABLE]
    return spreadable !== undefined ? !!spreadable : isArray(O)
  }

  const FORCED = !IS_CONCAT_SPREADABLE_SUPPORT || !SPECIES_SUPPORT

  // `Array.prototype.concat` method
  // https://tc39.es/ecma262/#sec-array.prototype.concat
  // with adding support of @@isConcatSpreadable and @@species
  _export({ target: 'Array', proto: true, forced: FORCED }, {
    // eslint-disable-next-line no-unused-vars -- required for `.length`
    concat: function concat (arg) {
      const O = toObject(this)
      const A = arraySpeciesCreate(O, 0)
      let n = 0
      let i, k, length, len, E
      for (i = -1, length = arguments.length; i < length; i++) {
        E = i === -1 ? O : arguments[i]
        if (isConcatSpreadable(E)) {
          len = toLength(E.length)
          if (n + len > MAX_SAFE_INTEGER) throw TypeError(MAXIMUM_ALLOWED_INDEX_EXCEEDED)
          for (k = 0; k < len; k++, n++) if (k in E) createProperty(A, n, E[k])
        } else {
          if (n >= MAX_SAFE_INTEGER) throw TypeError(MAXIMUM_ALLOWED_INDEX_EXCEEDED)
          createProperty(A, n++, E)
        }
      }
      A.length = n
      return A
    }
  })

  /**
   * @author: Dennis Hernández
   * @webSite: http://djhvscf.github.io/Blog
   * @update: https://github.com/wenzhixin
   * @version: v1.2.0
   */

  $__default.default.akottr.dragtable.prototype._restoreState = function (persistObj) {
    let i = 0

    for (let _i = 0, _Object$entries = Object.entries(persistObj); _i < _Object$entries.length; _i++) {
      const _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2)
      const field = _Object$entries$_i[0]
      const value = _Object$entries$_i[1]

      const $th = this.originalTable.el.find('th[data-field="'.concat(field, '"]'))

      if (!$th.length) {
        i++
        continue
      }

      this.originalTable.startIndex = $th.prevAll().length + 1
      this.originalTable.endIndex = parseInt(value, 10) + 1 - i

      this._bubbleCols()
    }
  } // From MDN site, https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter

  const filterFn = function filterFn () {
    if (!Array.prototype.filter) {
      Array.prototype.filter = function (fun
      /* , thisArg */
      ) {
        if (this === undefined || this === null) {
          throw new TypeError()
        }

        const t = Object(this)
        const len = t.length >>> 0

        if (typeof fun !== 'function') {
          throw new TypeError()
        }

        const res = []
        const thisArg = arguments.length >= 2 ? arguments[1] : undefined

        for (let i = 0; i < len; i++) {
          if (i in t) {
            const val = t[i] // NOTE: Technically this should Object.defineProperty at
            //       the next index, as push can be affected by
            //       properties on Object.prototype and Array.prototype.
            //       But this method's new, and collisions should be
            //       rare, so use the more-compatible alternative.

            if (fun.call(thisArg, val, i, t)) {
              res.push(val)
            }
          }
        }

        return res
      }
    }
  }

  $__default.default.extend($__default.default.fn.bootstrapTable.defaults, {
    reorderableColumns: false,
    maxMovingRows: 10,
    // eslint-disable-next-line no-unused-vars
    onReorderColumn: function onReorderColumn (headerFields) {
      return false
    },
    dragaccept: null
  })
  $__default.default.extend($__default.default.fn.bootstrapTable.Constructor.EVENTS, {
    'reorder-column.bs.table': 'onReorderColumn'
  })
  $__default.default.fn.bootstrapTable.methods.push('orderColumns')

  $__default.default.BootstrapTable = /* #__PURE__ */(function (_$$BootstrapTable) {
    _inherits(_class, _$$BootstrapTable)

    const _super = _createSuper(_class)

    function _class () {
      _classCallCheck(this, _class)

      return _super.apply(this, arguments)
    }

    _createClass(_class, [{
      key: 'initHeader',
      value: function initHeader () {
        let _get2

        for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
          args[_key] = arguments[_key]
        }

        (_get2 = _get(_getPrototypeOf(_class.prototype), 'initHeader', this)).call.apply(_get2, [this].concat(args))

        if (!this.options.reorderableColumns) {
          return
        }

        this.makeRowsReorderable()
      }
    }, {
      key: '_toggleColumn',
      value: function _toggleColumn () {
        let _get3

        for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
          args[_key2] = arguments[_key2]
        }

        (_get3 = _get(_getPrototypeOf(_class.prototype), '_toggleColumn', this)).call.apply(_get3, [this].concat(args))

        if (!this.options.reorderableColumns) {
          return
        }

        this.makeRowsReorderable()
      }
    }, {
      key: 'toggleView',
      value: function toggleView () {
        let _get4

        for (var _len3 = arguments.length, args = new Array(_len3), _key3 = 0; _key3 < _len3; _key3++) {
          args[_key3] = arguments[_key3]
        }

        (_get4 = _get(_getPrototypeOf(_class.prototype), 'toggleView', this)).call.apply(_get4, [this].concat(args))

        if (!this.options.reorderableColumns) {
          return
        }

        if (this.options.cardView) {
          return
        }

        this.makeRowsReorderable()
      }
    }, {
      key: 'resetView',
      value: function resetView () {
        let _get5

        for (var _len4 = arguments.length, args = new Array(_len4), _key4 = 0; _key4 < _len4; _key4++) {
          args[_key4] = arguments[_key4]
        }

        (_get5 = _get(_getPrototypeOf(_class.prototype), 'resetView', this)).call.apply(_get5, [this].concat(args))

        if (!this.options.reorderableColumns) {
          return
        }

        this.makeRowsReorderable()
      }
    }, {
      key: 'makeRowsReorderable',
      value: function makeRowsReorderable () {
        const _this = this

        const order = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null

        try {
          $__default.default(this.$el).dragtable('destroy')
        } catch (e) { // do nothing
        }

        $__default.default(this.$el).dragtable({
          maxMovingRows: this.options.maxMovingRows,
          dragaccept: this.options.dragaccept,
          clickDelay: 200,
          dragHandle: '.th-inner',
          restoreState: order || this.columnsSortOrder,
          beforeStop: function beforeStop (table) {
            const sortOrder = {}
            table.el.find('th').each(function (i, el) {
              sortOrder[$__default.default(el).data('field')] = i
            })
            _this.columnsSortOrder = sortOrder

            if (_this.options.cookie) {
              _this.persistReorderColumnsState(_this)
            }

            const ths = []
            const formatters = []
            const columns = []
            let columnsHidden = []
            let columnIndex = -1
            const optionsColumns = []

            _this.$header.find('th:not(.detail)').each(function (i, el) {
              ths.push($__default.default(el).data('field'))
              formatters.push($__default.default(el).data('formatter'))
            }) // Exist columns not shown

            if (ths.length < _this.columns.length) {
              columnsHidden = _this.columns.filter(function (column) {
                return !column.visible
              })

              for (let i = 0; i < columnsHidden.length; i++) {
                ths.push(columnsHidden[i].field)
                formatters.push(columnsHidden[i].formatter)
              }
            }

            for (let _i2 = 0; _i2 < ths.length; _i2++) {
              columnIndex = _this.fieldsColumnsIndex[ths[_i2]]

              if (columnIndex !== -1) {
                _this.fieldsColumnsIndex[ths[_i2]] = _i2
                _this.columns[columnIndex].fieldIndex = _i2
                columns.push(_this.columns[columnIndex])
              }
            }

            _this.columns = columns
            filterFn() // Support <IE9

            $__default.default.each(_this.columns, function (i, column) {
              let found = false
              const field = column.field

              _this.options.columns[0].filter(function (item) {
                if (!found && item.field === field) {
                  optionsColumns.push(item)
                  found = true
                  return false
                }

                return true
              })
            })
            _this.options.columns[0] = optionsColumns
            _this.header.fields = ths
            _this.header.formatters = formatters

            _this.initHeader()

            _this.initToolbar()

            _this.initSearchText()

            _this.initBody()

            _this.resetView()

            _this.trigger('reorder-column', ths)
          }
        })
      }
    }, {
      key: 'orderColumns',
      value: function orderColumns (order) {
        this.columnsSortOrder = order
        this.makeRowsReorderable()
      }
    }])

    return _class
  }($__default.default.BootstrapTable))
}))
