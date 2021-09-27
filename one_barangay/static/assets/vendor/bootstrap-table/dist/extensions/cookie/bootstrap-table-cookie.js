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

  function _createForOfIteratorHelper (o, allowArrayLike) {
    let it

    if (typeof Symbol === 'undefined' || o[Symbol.iterator] == null) {
      if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === 'number') {
        if (it) o = it
        let i = 0

        const F = function () {}

        return {
          s: F,
          n: function () {
            if (i >= o.length) {
              return {
                done: true
              }
            }
            return {
              done: false,
              value: o[i++]
            }
          },
          e: function (e) {
            throw e
          },
          f: F
        }
      }

      throw new TypeError('Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.')
    }

    let normalCompletion = true
    let didErr = false
    let err
    return {
      s: function () {
        it = o[Symbol.iterator]()
      },
      n: function () {
        const step = it.next()
        normalCompletion = step.done
        return step
      },
      e: function (e) {
        didErr = true
        err = e
      },
      f: function () {
        try {
          if (!normalCompletion && it.return != null) it.return()
        } finally {
          if (didErr) throw err
        }
      }
    }
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
  const floor$1 = Math.floor

  // `ToInteger` abstract operation
  // https://tc39.es/ecma262/#sec-tointeger
  const toInteger = function (argument) {
    return isNaN(argument = +argument) ? 0 : (argument > 0 ? floor$1 : ceil)(argument)
  }

  const min$3 = Math.min

  // `ToLength` abstract operation
  // https://tc39.es/ecma262/#sec-tolength
  const toLength = function (argument) {
    return argument > 0 ? min$3(toInteger(argument), 0x1FFFFFFFFFFFFF) : 0 // 2 ** 53 - 1 == 9007199254740991
  }

  const max$1 = Math.max
  const min$2 = Math.min

  // Helper for a popular repeating case of the spec:
  // Let integer be ? ToInteger(index).
  // If integer < 0, let result be max((length + integer), 0); else let result be min(integer, length).
  const toAbsoluteIndex = function (index, length) {
    const integer = toInteger(index)
    return integer < 0 ? max$1(integer + length, 0) : min$2(integer, length)
  }

  // `Array.prototype.{ indexOf, includes }` methods implementation
  const createMethod$2 = function (IS_INCLUDES) {
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
    includes: createMethod$2(true),
    // `Array.prototype.indexOf` method
    // https://tc39.es/ecma262/#sec-array.prototype.indexof
    indexOf: createMethod$2(false)
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

  // `IsArray` abstract operation
  // https://tc39.es/ecma262/#sec-isarray
  const isArray = Array.isArray || function isArray (arg) {
    return classofRaw(arg) == 'Array'
  }

  // `ToObject` abstract operation
  // https://tc39.es/ecma262/#sec-toobject
  const toObject = function (argument) {
    return Object(requireObjectCoercible(argument))
  }

  const createProperty = function (object, key, value) {
    const propertyKey = toPrimitive(key)
    if (propertyKey in object) objectDefineProperty.f(object, propertyKey, createPropertyDescriptor(0, value))
    else object[propertyKey] = value
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

  const SPECIES$3 = wellKnownSymbol('species')

  // `ArraySpeciesCreate` abstract operation
  // https://tc39.es/ecma262/#sec-arrayspeciescreate
  const arraySpeciesCreate = function (originalArray, length) {
    let C
    if (isArray(originalArray)) {
      C = originalArray.constructor
      // cross-realm fallback
      if (typeof C === 'function' && (C === Array || isArray(C.prototype))) C = undefined
      else if (isObject(C)) {
        C = C[SPECIES$3]
        if (C === null) C = undefined
      }
    } return new (C === undefined ? Array : C)(length === 0 ? 0 : length)
  }

  const SPECIES$2 = wellKnownSymbol('species')

  const arrayMethodHasSpeciesSupport = function (METHOD_NAME) {
    // We can't use this feature detection in V8 since it causes
    // deoptimization and serious performance degradation
    // https://github.com/zloirock/core-js/issues/677
    return engineV8Version >= 51 || !fails(function () {
      const array = []
      const constructor = array.constructor = {}
      constructor[SPECIES$2] = function () {
        return { foo: 1 }
      }
      return array[METHOD_NAME](Boolean).foo !== 1
    })
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

  const arrayMethodIsStrict = function (METHOD_NAME, argument) {
    const method = [][METHOD_NAME]
    return !!method && fails(function () {
      // eslint-disable-next-line no-useless-call,no-throw-literal -- required for testing
      method.call(null, argument || function () { throw 1 }, 1)
    })
  }

  const nativeJoin = [].join

  const ES3_STRINGS = indexedObject != Object
  const STRICT_METHOD$1 = arrayMethodIsStrict('join', ',')

  // `Array.prototype.join` method
  // https://tc39.es/ecma262/#sec-array.prototype.join
  _export({ target: 'Array', proto: true, forced: ES3_STRINGS || !STRICT_METHOD$1 }, {
    join: function join (separator) {
      return nativeJoin.call(toIndexedObject(this), separator === undefined ? ',' : separator)
    }
  })

  // `RegExp.prototype.flags` getter implementation
  // https://tc39.es/ecma262/#sec-get-regexp.prototype.flags
  const regexpFlags = function () {
    const that = anObject(this)
    let result = ''
    if (that.global) result += 'g'
    if (that.ignoreCase) result += 'i'
    if (that.multiline) result += 'm'
    if (that.dotAll) result += 's'
    if (that.unicode) result += 'u'
    if (that.sticky) result += 'y'
    return result
  }

  // babel-minify transpiles RegExp('a', 'y') -> /a/y and it causes SyntaxError,
  // so we use an intermediate function.
  function RE (s, f) {
    return RegExp(s, f)
  }

  const UNSUPPORTED_Y$1 = fails(function () {
    // babel-minify transpiles RegExp('a', 'y') -> /a/y and it causes SyntaxError
    const re = RE('a', 'y')
    re.lastIndex = 2
    return re.exec('abcd') != null
  })

  const BROKEN_CARET = fails(function () {
    // https://bugzilla.mozilla.org/show_bug.cgi?id=773687
    const re = RE('^r', 'gy')
    re.lastIndex = 2
    return re.exec('str') != null
  })

  const regexpStickyHelpers = {
  	UNSUPPORTED_Y: UNSUPPORTED_Y$1,
  	BROKEN_CARET: BROKEN_CARET
  }

  const nativeExec = RegExp.prototype.exec
  // This always refers to the native implementation, because the
  // String#replace polyfill uses ./fix-regexp-well-known-symbol-logic.js,
  // which loads this file before patching the method.
  const nativeReplace = String.prototype.replace

  let patchedExec = nativeExec

  const UPDATES_LAST_INDEX_WRONG = (function () {
    const re1 = /a/
    const re2 = /b*/g
    nativeExec.call(re1, 'a')
    nativeExec.call(re2, 'a')
    return re1.lastIndex !== 0 || re2.lastIndex !== 0
  })()

  const UNSUPPORTED_Y = regexpStickyHelpers.UNSUPPORTED_Y || regexpStickyHelpers.BROKEN_CARET

  // nonparticipating capturing group, copied from es5-shim's String#split patch.
  // eslint-disable-next-line regexp/no-assertion-capturing-group, regexp/no-empty-group -- required for testing
  const NPCG_INCLUDED = /()??/.exec('')[1] !== undefined

  const PATCH = UPDATES_LAST_INDEX_WRONG || NPCG_INCLUDED || UNSUPPORTED_Y

  if (PATCH) {
    patchedExec = function exec (str) {
      const re = this
      let lastIndex, reCopy, match, i
      const sticky = UNSUPPORTED_Y && re.sticky
      let flags = regexpFlags.call(re)
      let source = re.source
      let charsAdded = 0
      let strCopy = str

      if (sticky) {
        flags = flags.replace('y', '')
        if (flags.indexOf('g') === -1) {
          flags += 'g'
        }

        strCopy = String(str).slice(re.lastIndex)
        // Support anchored sticky behavior.
        if (re.lastIndex > 0 && (!re.multiline || re.multiline && str[re.lastIndex - 1] !== '\n')) {
          source = '(?: ' + source + ')'
          strCopy = ' ' + strCopy
          charsAdded++
        }
        // ^(? + rx + ) is needed, in combination with some str slicing, to
        // simulate the 'y' flag.
        reCopy = new RegExp('^(?:' + source + ')', flags)
      }

      if (NPCG_INCLUDED) {
        reCopy = new RegExp('^' + source + '$(?!\\s)', flags)
      }
      if (UPDATES_LAST_INDEX_WRONG) lastIndex = re.lastIndex

      match = nativeExec.call(sticky ? reCopy : re, strCopy)

      if (sticky) {
        if (match) {
          match.input = match.input.slice(charsAdded)
          match[0] = match[0].slice(charsAdded)
          match.index = re.lastIndex
          re.lastIndex += match[0].length
        } else re.lastIndex = 0
      } else if (UPDATES_LAST_INDEX_WRONG && match) {
        re.lastIndex = re.global ? match.index + match[0].length : lastIndex
      }
      if (NPCG_INCLUDED && match && match.length > 1) {
        // Fix browsers whose `exec` methods don't consistently return `undefined`
        // for NPCG, like IE8. NOTE: This doesn' work for /(.?)?/
        nativeReplace.call(match[0], reCopy, function () {
          for (i = 1; i < arguments.length - 2; i++) {
            if (arguments[i] === undefined) match[i] = undefined
          }
        })
      }

      return match
    }
  }

  const regexpExec = patchedExec

  // `RegExp.prototype.exec` method
  // https://tc39.es/ecma262/#sec-regexp.prototype.exec
  _export({ target: 'RegExp', proto: true, forced: /./.exec !== regexpExec }, {
    exec: regexpExec
  })

  // TODO: Remove from `core-js@4` since it's moved to entry points

  const SPECIES$1 = wellKnownSymbol('species')

  const REPLACE_SUPPORTS_NAMED_GROUPS = !fails(function () {
    // #replace needs built-in support for named groups.
    // #match works fine because it just return the exec results, even if it has
    // a "grops" property.
    const re = /./
    re.exec = function () {
      const result = []
      result.groups = { a: '7' }
      return result
    }
    return ''.replace(re, '$<a>') !== '7'
  })

  // IE <= 11 replaces $0 with the whole match, as if it was $&
  // https://stackoverflow.com/questions/6024666/getting-ie-to-replace-a-regex-with-the-literal-string-0
  const REPLACE_KEEPS_$0 = (function () {
    return 'a'.replace(/./, '$0') === '$0'
  })()

  const REPLACE = wellKnownSymbol('replace')
  // Safari <= 13.0.3(?) substitutes nth capture where n>m with an empty string
  const REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE = (function () {
    if (/./[REPLACE]) {
      return /./[REPLACE]('a', '$0') === ''
    }
    return false
  })()

  // Chrome 51 has a buggy "split" implementation when RegExp#exec !== nativeExec
  // Weex JS has frozen built-in prototypes, so use try / catch wrapper
  const SPLIT_WORKS_WITH_OVERWRITTEN_EXEC = !fails(function () {
    // eslint-disable-next-line regexp/no-empty-group -- required for testing
    const re = /(?:)/
    const originalExec = re.exec
    re.exec = function () { return originalExec.apply(this, arguments) }
    const result = 'ab'.split(re)
    return result.length !== 2 || result[0] !== 'a' || result[1] !== 'b'
  })

  const fixRegexpWellKnownSymbolLogic = function (KEY, length, exec, sham) {
    const SYMBOL = wellKnownSymbol(KEY)

    const DELEGATES_TO_SYMBOL = !fails(function () {
      // String methods call symbol-named RegEp methods
      const O = {}
      O[SYMBOL] = function () { return 7 }
      return ''[KEY](O) != 7
    })

    const DELEGATES_TO_EXEC = DELEGATES_TO_SYMBOL && !fails(function () {
      // Symbol-named RegExp methods call .exec
      let execCalled = false
      let re = /a/

      if (KEY === 'split') {
        // We can't use real regex here since it causes deoptimization
        // and serious performance degradation in V8
        // https://github.com/zloirock/core-js/issues/306
        re = {}
        // RegExp[@@split] doesn't call the regex's exec method, but first creates
        // a new one. We need to return the patched regex when creating the new one.
        re.constructor = {}
        re.constructor[SPECIES$1] = function () { return re }
        re.flags = ''
        re[SYMBOL] = /./[SYMBOL]
      }

      re.exec = function () { execCalled = true; return null }

      re[SYMBOL]('')
      return !execCalled
    })

    if (
      !DELEGATES_TO_SYMBOL ||
      !DELEGATES_TO_EXEC ||
      (KEY === 'replace' && !(
        REPLACE_SUPPORTS_NAMED_GROUPS &&
        REPLACE_KEEPS_$0 &&
        !REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE
      )) ||
      (KEY === 'split' && !SPLIT_WORKS_WITH_OVERWRITTEN_EXEC)
    ) {
      const nativeRegExpMethod = /./[SYMBOL]
      const methods = exec(SYMBOL, ''[KEY], function (nativeMethod, regexp, str, arg2, forceStringMethod) {
        if (regexp.exec === regexpExec) {
          if (DELEGATES_TO_SYMBOL && !forceStringMethod) {
            // The native String method already delegates to @@method (this
            // polyfilled function), leasing to infinite recursion.
            // We avoid it by directly calling the native @@method method.
            return { done: true, value: nativeRegExpMethod.call(regexp, str, arg2) }
          }
          return { done: true, value: nativeMethod.call(str, regexp, arg2) }
        }
        return { done: false }
      }, {
        REPLACE_KEEPS_$0: REPLACE_KEEPS_$0,
        REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE: REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE
      })
      const stringMethod = methods[0]
      const regexMethod = methods[1]

      redefine(String.prototype, KEY, stringMethod)
      redefine(RegExp.prototype, SYMBOL, length == 2
        // 21.2.5.8 RegExp.prototype[@@replace](string, replaceValue)
        // 21.2.5.11 RegExp.prototype[@@split](string, limit)
        ? function (string, arg) { return regexMethod.call(string, this, arg) }
        // 21.2.5.6 RegExp.prototype[@@match](string)
        // 21.2.5.9 RegExp.prototype[@@search](string)
        : function (string) { return regexMethod.call(string, this) }
      )
    }

    if (sham) createNonEnumerableProperty(RegExp.prototype[SYMBOL], 'sham', true)
  }

  const MATCH = wellKnownSymbol('match')

  // `IsRegExp` abstract operation
  // https://tc39.es/ecma262/#sec-isregexp
  const isRegexp = function (it) {
    let isRegExp
    return isObject(it) && ((isRegExp = it[MATCH]) !== undefined ? !!isRegExp : classofRaw(it) == 'RegExp')
  }

  const aFunction = function (it) {
    if (typeof it !== 'function') {
      throw TypeError(String(it) + ' is not a function')
    } return it
  }

  const SPECIES = wellKnownSymbol('species')

  // `SpeciesConstructor` abstract operation
  // https://tc39.es/ecma262/#sec-speciesconstructor
  const speciesConstructor = function (O, defaultConstructor) {
    const C = anObject(O).constructor
    let S
    return C === undefined || (S = anObject(C)[SPECIES]) == undefined ? defaultConstructor : aFunction(S)
  }

  // `String.prototype.{ codePointAt, at }` methods implementation
  const createMethod$1 = function (CONVERT_TO_STRING) {
    return function ($this, pos) {
      const S = String(requireObjectCoercible($this))
      const position = toInteger(pos)
      const size = S.length
      let first, second
      if (position < 0 || position >= size) return CONVERT_TO_STRING ? '' : undefined
      first = S.charCodeAt(position)
      return first < 0xD800 || first > 0xDBFF || position + 1 === size ||
        (second = S.charCodeAt(position + 1)) < 0xDC00 || second > 0xDFFF
        ? CONVERT_TO_STRING ? S.charAt(position) : first
        : CONVERT_TO_STRING ? S.slice(position, position + 2) : (first - 0xD800 << 10) + (second - 0xDC00) + 0x10000
    }
  }

  const stringMultibyte = {
    // `String.prototype.codePointAt` method
    // https://tc39.es/ecma262/#sec-string.prototype.codepointat
    codeAt: createMethod$1(false),
    // `String.prototype.at` method
    // https://github.com/mathiasbynens/String.prototype.at
    charAt: createMethod$1(true)
  }

  const charAt = stringMultibyte.charAt

  // `AdvanceStringIndex` abstract operation
  // https://tc39.es/ecma262/#sec-advancestringindex
  const advanceStringIndex = function (S, index, unicode) {
    return index + (unicode ? charAt(S, index).length : 1)
  }

  // `RegExpExec` abstract operation
  // https://tc39.es/ecma262/#sec-regexpexec
  const regexpExecAbstract = function (R, S) {
    const exec = R.exec
    if (typeof exec === 'function') {
      const result = exec.call(R, S)
      if (typeof result !== 'object') {
        throw TypeError('RegExp exec method returned something other than an Object or null')
      }
      return result
    }

    if (classofRaw(R) !== 'RegExp') {
      throw TypeError('RegExp#exec called on incompatible receiver')
    }

    return regexpExec.call(R, S)
  }

  const arrayPush = [].push
  const min$1 = Math.min
  const MAX_UINT32 = 0xFFFFFFFF

  // babel-minify transpiles RegExp('x', 'y') -> /x/y and it causes SyntaxError
  const SUPPORTS_Y = !fails(function () { return !RegExp(MAX_UINT32, 'y') })

  // @@split logic
  fixRegexpWellKnownSymbolLogic('split', 2, function (SPLIT, nativeSplit, maybeCallNative) {
    let internalSplit
    if (
      'abbc'.split(/(b)*/)[1] == 'c' ||
      // eslint-disable-next-line regexp/no-empty-group -- required for testing
      'test'.split(/(?:)/, -1).length != 4 ||
      'ab'.split(/(?:ab)*/).length != 2 ||
      '.'.split(/(.?)(.?)/).length != 4 ||
      // eslint-disable-next-line regexp/no-assertion-capturing-group, regexp/no-empty-group -- required for testing
      '.'.split(/()()/).length > 1 ||
      ''.split(/.?/).length
    ) {
      // based on es5-shim implementation, need to rework it
      internalSplit = function (separator, limit) {
        const string = String(requireObjectCoercible(this))
        const lim = limit === undefined ? MAX_UINT32 : limit >>> 0
        if (lim === 0) return []
        if (separator === undefined) return [string]
        // If `separator` is not a regex, use native split
        if (!isRegexp(separator)) {
          return nativeSplit.call(string, separator, lim)
        }
        const output = []
        const flags = (separator.ignoreCase ? 'i' : '') +
                    (separator.multiline ? 'm' : '') +
                    (separator.unicode ? 'u' : '') +
                    (separator.sticky ? 'y' : '')
        let lastLastIndex = 0
        // Make `global` and avoid `lastIndex` issues by working with a copy
        const separatorCopy = new RegExp(separator.source, flags + 'g')
        let match, lastIndex, lastLength
        while (match = regexpExec.call(separatorCopy, string)) {
          lastIndex = separatorCopy.lastIndex
          if (lastIndex > lastLastIndex) {
            output.push(string.slice(lastLastIndex, match.index))
            if (match.length > 1 && match.index < string.length) arrayPush.apply(output, match.slice(1))
            lastLength = match[0].length
            lastLastIndex = lastIndex
            if (output.length >= lim) break
          }
          if (separatorCopy.lastIndex === match.index) separatorCopy.lastIndex++ // Avoid an infinite loop
        }
        if (lastLastIndex === string.length) {
          if (lastLength || !separatorCopy.test('')) output.push('')
        } else output.push(string.slice(lastLastIndex))
        return output.length > lim ? output.slice(0, lim) : output
      }
    // Chakra, V8
    } else if ('0'.split(undefined, 0).length) {
      internalSplit = function (separator, limit) {
        return separator === undefined && limit === 0 ? [] : nativeSplit.call(this, separator, limit)
      }
    } else internalSplit = nativeSplit

    return [
      // `String.prototype.split` method
      // https://tc39.es/ecma262/#sec-string.prototype.split
      function split (separator, limit) {
        const O = requireObjectCoercible(this)
        const splitter = separator == undefined ? undefined : separator[SPLIT]
        return splitter !== undefined
          ? splitter.call(separator, O, limit)
          : internalSplit.call(String(O), separator, limit)
      },
      // `RegExp.prototype[@@split]` method
      // https://tc39.es/ecma262/#sec-regexp.prototype-@@split
      //
      // NOTE: This cannot be properly polyfilled in engines that don't support
      // the 'y' flag.
      function (regexp, limit) {
        const res = maybeCallNative(internalSplit, regexp, this, limit, internalSplit !== nativeSplit)
        if (res.done) return res.value

        const rx = anObject(regexp)
        const S = String(this)
        const C = speciesConstructor(rx, RegExp)

        const unicodeMatching = rx.unicode
        const flags = (rx.ignoreCase ? 'i' : '') +
                    (rx.multiline ? 'm' : '') +
                    (rx.unicode ? 'u' : '') +
                    (SUPPORTS_Y ? 'y' : 'g')

        // ^(? + rx + ) is needed, in combination with some S slicing, to
        // simulate the 'y' flag.
        const splitter = new C(SUPPORTS_Y ? rx : '^(?:' + rx.source + ')', flags)
        const lim = limit === undefined ? MAX_UINT32 : limit >>> 0
        if (lim === 0) return []
        if (S.length === 0) return regexpExecAbstract(splitter, S) === null ? [S] : []
        let p = 0
        let q = 0
        const A = []
        while (q < S.length) {
          splitter.lastIndex = SUPPORTS_Y ? q : 0
          const z = regexpExecAbstract(splitter, SUPPORTS_Y ? S : S.slice(q))
          var e
          if (
            z === null ||
            (e = min$1(toLength(splitter.lastIndex + (SUPPORTS_Y ? 0 : q)), S.length)) === p
          ) {
            q = advanceStringIndex(S, q, unicodeMatching)
          } else {
            A.push(S.slice(p, q))
            if (A.length === lim) return A
            for (let i = 1; i <= z.length - 1; i++) {
              A.push(z[i])
              if (A.length === lim) return A
            }
            q = p = e
          }
        }
        A.push(S.slice(p))
        return A
      }
    ]
  }, !SUPPORTS_Y)

  const floor = Math.floor
  const replace = ''.replace
  const SUBSTITUTION_SYMBOLS = /\$([$&'`]|\d{1,2}|<[^>]*>)/g
  const SUBSTITUTION_SYMBOLS_NO_NAMED = /\$([$&'`]|\d{1,2})/g

  // https://tc39.es/ecma262/#sec-getsubstitution
  const getSubstitution = function (matched, str, position, captures, namedCaptures, replacement) {
    const tailPos = position + matched.length
    const m = captures.length
    let symbols = SUBSTITUTION_SYMBOLS_NO_NAMED
    if (namedCaptures !== undefined) {
      namedCaptures = toObject(namedCaptures)
      symbols = SUBSTITUTION_SYMBOLS
    }
    return replace.call(replacement, symbols, function (match, ch) {
      let capture
      switch (ch.charAt(0)) {
        case '$': return '$'
        case '&': return matched
        case '`': return str.slice(0, position)
        case "'": return str.slice(tailPos)
        case '<':
          capture = namedCaptures[ch.slice(1, -1)]
          break
        default: // \d\d?
          var n = +ch
          if (n === 0) return match
          if (n > m) {
            const f = floor(n / 10)
            if (f === 0) return match
            if (f <= m) return captures[f - 1] === undefined ? ch.charAt(1) : captures[f - 1] + ch.charAt(1)
            return match
          }
          capture = captures[n - 1]
      }
      return capture === undefined ? '' : capture
    })
  }

  const max = Math.max
  const min = Math.min

  const maybeToString = function (it) {
    return it === undefined ? it : String(it)
  }

  // @@replace logic
  fixRegexpWellKnownSymbolLogic('replace', 2, function (REPLACE, nativeReplace, maybeCallNative, reason) {
    const REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE = reason.REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE
    const REPLACE_KEEPS_$0 = reason.REPLACE_KEEPS_$0
    const UNSAFE_SUBSTITUTE = REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE ? '$' : '$0'

    return [
      // `String.prototype.replace` method
      // https://tc39.es/ecma262/#sec-string.prototype.replace
      function replace (searchValue, replaceValue) {
        const O = requireObjectCoercible(this)
        const replacer = searchValue == undefined ? undefined : searchValue[REPLACE]
        return replacer !== undefined
          ? replacer.call(searchValue, O, replaceValue)
          : nativeReplace.call(String(O), searchValue, replaceValue)
      },
      // `RegExp.prototype[@@replace]` method
      // https://tc39.es/ecma262/#sec-regexp.prototype-@@replace
      function (regexp, replaceValue) {
        if (
          (!REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE && REPLACE_KEEPS_$0) ||
          (typeof replaceValue === 'string' && replaceValue.indexOf(UNSAFE_SUBSTITUTE) === -1)
        ) {
          const res = maybeCallNative(nativeReplace, regexp, this, replaceValue)
          if (res.done) return res.value
        }

        const rx = anObject(regexp)
        const S = String(this)

        const functionalReplace = typeof replaceValue === 'function'
        if (!functionalReplace) replaceValue = String(replaceValue)

        const global = rx.global
        if (global) {
          var fullUnicode = rx.unicode
          rx.lastIndex = 0
        }
        const results = []
        while (true) {
          var result = regexpExecAbstract(rx, S)
          if (result === null) break

          results.push(result)
          if (!global) break

          const matchStr = String(result[0])
          if (matchStr === '') rx.lastIndex = advanceStringIndex(S, toLength(rx.lastIndex), fullUnicode)
        }

        let accumulatedResult = ''
        let nextSourcePosition = 0
        for (let i = 0; i < results.length; i++) {
          result = results[i]

          const matched = String(result[0])
          const position = max(min(toInteger(result.index), S.length), 0)
          const captures = []
          // NOTE: This is equivalent to
          //   captures = result.slice(1).map(maybeToString)
          // but for some reason `nativeSlice.call(result, 1, result.length)` (called in
          // the slice polyfill when slicing native arrays) "doesn't work" in safari 9 and
          // causes a crash (https://pastebin.com/N21QzeQA) when trying to debug it.
          for (let j = 1; j < result.length; j++) captures.push(maybeToString(result[j]))
          const namedCaptures = result.groups
          if (functionalReplace) {
            const replacerArgs = [matched].concat(captures, position, S)
            if (namedCaptures !== undefined) replacerArgs.push(namedCaptures)
            var replacement = String(replaceValue.apply(undefined, replacerArgs))
          } else {
            replacement = getSubstitution(matched, S, position, captures, namedCaptures, replaceValue)
          }
          if (position >= nextSourcePosition) {
            accumulatedResult += S.slice(nextSourcePosition, position) + replacement
            nextSourcePosition = position + matched.length
          }
        }
        return accumulatedResult + S.slice(nextSourcePosition)
      }
    ]
  })

  // iterable DOM collections
  // flag - `iterable` interface - 'entries', 'keys', 'values', 'forEach' methods
  const domIterables = {
    CSSRuleList: 0,
    CSSStyleDeclaration: 0,
    CSSValueList: 0,
    ClientRectList: 0,
    DOMRectList: 0,
    DOMStringList: 0,
    DOMTokenList: 1,
    DataTransferItemList: 0,
    FileList: 0,
    HTMLAllCollection: 0,
    HTMLCollection: 0,
    HTMLFormElement: 0,
    HTMLSelectElement: 0,
    MediaList: 0,
    MimeTypeArray: 0,
    NamedNodeMap: 0,
    NodeList: 1,
    PaintRequestList: 0,
    Plugin: 0,
    PluginArray: 0,
    SVGLengthList: 0,
    SVGNumberList: 0,
    SVGPathSegList: 0,
    SVGPointList: 0,
    SVGStringList: 0,
    SVGTransformList: 0,
    SourceBufferList: 0,
    StyleSheetList: 0,
    TextTrackCueList: 0,
    TextTrackList: 0,
    TouchList: 0
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

  const push = [].push

  // `Array.prototype.{ forEach, map, filter, some, every, find, findIndex, filterOut }` methods implementation
  const createMethod = function (TYPE) {
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
    forEach: createMethod(0),
    // `Array.prototype.map` method
    // https://tc39.es/ecma262/#sec-array.prototype.map
    map: createMethod(1),
    // `Array.prototype.filter` method
    // https://tc39.es/ecma262/#sec-array.prototype.filter
    filter: createMethod(2),
    // `Array.prototype.some` method
    // https://tc39.es/ecma262/#sec-array.prototype.some
    some: createMethod(3),
    // `Array.prototype.every` method
    // https://tc39.es/ecma262/#sec-array.prototype.every
    every: createMethod(4),
    // `Array.prototype.find` method
    // https://tc39.es/ecma262/#sec-array.prototype.find
    find: createMethod(5),
    // `Array.prototype.findIndex` method
    // https://tc39.es/ecma262/#sec-array.prototype.findIndex
    findIndex: createMethod(6),
    // `Array.prototype.filterOut` method
    // https://github.com/tc39/proposal-array-filtering
    filterOut: createMethod(7)
  }

  const $forEach = arrayIteration.forEach

  const STRICT_METHOD = arrayMethodIsStrict('forEach')

  // `Array.prototype.forEach` method implementation
  // https://tc39.es/ecma262/#sec-array.prototype.foreach
  const arrayForEach = !STRICT_METHOD ? function forEach (callbackfn /* , thisArg */) {
    return $forEach(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined)
  } : [].forEach

  for (const COLLECTION_NAME in domIterables) {
    const Collection = global_1[COLLECTION_NAME]
    const CollectionPrototype = Collection && Collection.prototype
    // some Chrome versions have non-configurable methods on DOMTokenList
    if (CollectionPrototype && CollectionPrototype.forEach !== arrayForEach) {
      try {
        createNonEnumerableProperty(CollectionPrototype, 'forEach', arrayForEach)
      } catch (error) {
        CollectionPrototype.forEach = arrayForEach
      }
    }
  }

  const TO_STRING_TAG$1 = wellKnownSymbol('toStringTag')
  const test = {}

  test[TO_STRING_TAG$1] = 'z'

  const toStringTagSupport = String(test) === '[object z]'

  const TO_STRING_TAG = wellKnownSymbol('toStringTag')
  // ES3 wrong here
  const CORRECT_ARGUMENTS = classofRaw(function () { return arguments }()) == 'Arguments'

  // fallback for IE11 Script Access Denied error
  const tryGet = function (it, key) {
    try {
      return it[key]
    } catch (error) { /* empty */ }
  }

  // getting tag from ES6+ `Object.prototype.toString`
  const classof = toStringTagSupport ? classofRaw : function (it) {
    let O, tag, result
    return it === undefined ? 'Undefined' : it === null ? 'Null'
      // @@toStringTag case
      : typeof (tag = tryGet(O = Object(it), TO_STRING_TAG)) === 'string' ? tag
      // builtinTag case
        : CORRECT_ARGUMENTS ? classofRaw(O)
        // ES3 arguments fallback
          : (result = classofRaw(O)) == 'Object' && typeof O.callee === 'function' ? 'Arguments' : result
  }

  // `Object.prototype.toString` method implementation
  // https://tc39.es/ecma262/#sec-object.prototype.tostring
  const objectToString = toStringTagSupport ? {}.toString : function toString () {
    return '[object ' + classof(this) + ']'
  }

  // `Object.prototype.toString` method
  // https://tc39.es/ecma262/#sec-object.prototype.tostring
  if (!toStringTagSupport) {
    redefine(Object.prototype, 'toString', objectToString, { unsafe: true })
  }

  const TO_STRING = 'toString'
  const RegExpPrototype = RegExp.prototype
  const nativeToString = RegExpPrototype[TO_STRING]

  const NOT_GENERIC = fails(function () { return nativeToString.call({ source: 'a', flags: 'b' }) != '/a/b' })
  // FF44- RegExp#toString has a wrong name
  const INCORRECT_NAME = nativeToString.name != TO_STRING

  // `RegExp.prototype.toString` method
  // https://tc39.es/ecma262/#sec-regexp.prototype.tostring
  if (NOT_GENERIC || INCORRECT_NAME) {
    redefine(RegExp.prototype, TO_STRING, function toString () {
      const R = anObject(this)
      const p = String(R.source)
      const rf = R.flags
      const f = String(rf === undefined && R instanceof RegExp && !('flags' in RegExpPrototype) ? regexpFlags.call(R) : rf)
      return '/' + p + '/' + f
    }, { unsafe: true })
  }

  // `Object.keys` method
  // https://tc39.es/ecma262/#sec-object.keys
  const objectKeys = Object.keys || function keys (O) {
    return objectKeysInternal(O, enumBugKeys)
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

  const $filter = arrayIteration.filter

  const HAS_SPECIES_SUPPORT$1 = arrayMethodHasSpeciesSupport('filter')

  // `Array.prototype.filter` method
  // https://tc39.es/ecma262/#sec-array.prototype.filter
  // with adding support of @@species
  _export({ target: 'Array', proto: true, forced: !HAS_SPECIES_SUPPORT$1 }, {
    filter: function filter (callbackfn /* , thisArg */) {
      return $filter(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined)
    }
  })

  const $map = arrayIteration.map

  const HAS_SPECIES_SUPPORT = arrayMethodHasSpeciesSupport('map')

  // `Array.prototype.map` method
  // https://tc39.es/ecma262/#sec-array.prototype.map
  // with adding support of @@species
  _export({ target: 'Array', proto: true, forced: !HAS_SPECIES_SUPPORT }, {
    map: function map (callbackfn /* , thisArg */) {
      return $map(this, callbackfn, arguments.length > 1 ? arguments[1] : undefined)
    }
  })

  // `SameValue` abstract operation
  // https://tc39.es/ecma262/#sec-samevalue
  const sameValue = Object.is || function is (x, y) {
    // eslint-disable-next-line no-self-compare -- NaN check
    return x === y ? x !== 0 || 1 / x === 1 / y : x != x && y != y
  }

  // @@search logic
  fixRegexpWellKnownSymbolLogic('search', 1, function (SEARCH, nativeSearch, maybeCallNative) {
    return [
      // `String.prototype.search` method
      // https://tc39.es/ecma262/#sec-string.prototype.search
      function search (regexp) {
        const O = requireObjectCoercible(this)
        const searcher = regexp == undefined ? undefined : regexp[SEARCH]
        return searcher !== undefined ? searcher.call(regexp, O) : new RegExp(regexp)[SEARCH](String(O))
      },
      // `RegExp.prototype[@@search]` method
      // https://tc39.es/ecma262/#sec-regexp.prototype-@@search
      function (regexp) {
        const res = maybeCallNative(nativeSearch, regexp, this)
        if (res.done) return res.value

        const rx = anObject(regexp)
        const S = String(this)

        const previousLastIndex = rx.lastIndex
        if (!sameValue(previousLastIndex, 0)) rx.lastIndex = 0
        const result = regexpExecAbstract(rx, S)
        if (!sameValue(rx.lastIndex, previousLastIndex)) rx.lastIndex = previousLastIndex
        return result === null ? -1 : result.index
      }
    ]
  })

  /**
   * @author: Dennis Hernández
   * @webSite: http://djhvscf.github.io/Blog
   * @update zhixin wen <wenzhixin2010@gmail.com>
   */

  const Utils = $__default.default.fn.bootstrapTable.utils
  var UtilsCookie = {
    cookieIds: {
      sortOrder: 'bs.table.sortOrder',
      sortName: 'bs.table.sortName',
      pageNumber: 'bs.table.pageNumber',
      pageList: 'bs.table.pageList',
      columns: 'bs.table.columns',
      searchText: 'bs.table.searchText',
      reorderColumns: 'bs.table.reorderColumns',
      filterControl: 'bs.table.filterControl',
      filterBy: 'bs.table.filterBy'
    },
    getCurrentHeader: function getCurrentHeader (that) {
      let header = that.$header

      if (that.options.height) {
        header = that.$tableHeader
      }

      return header
    },
    getCurrentSearchControls: function getCurrentSearchControls (that) {
      let searchControls = 'select, input'

      if (that.options.height) {
        searchControls = 'table select, table input'
      }

      return searchControls
    },
    cookieEnabled: function cookieEnabled () {
      return !!navigator.cookieEnabled
    },
    inArrayCookiesEnabled: function inArrayCookiesEnabled (cookieName, cookiesEnabled) {
      let index = -1

      for (let i = 0; i < cookiesEnabled.length; i++) {
        if (cookieName.toLowerCase() === cookiesEnabled[i].toLowerCase()) {
          index = i
          break
        }
      }

      return index
    },
    setCookie: function setCookie (that, cookieName, cookieValue) {
      if (!that.options.cookie || !UtilsCookie.cookieEnabled() || that.options.cookieIdTable === '') {
        return
      }

      if (UtilsCookie.inArrayCookiesEnabled(cookieName, that.options.cookiesEnabled) === -1) {
        return
      }

      cookieName = ''.concat(that.options.cookieIdTable, '.').concat(cookieName)

      switch (that.options.cookieStorage) {
        case 'cookieStorage':
          document.cookie = [cookieName, '=', encodeURIComponent(cookieValue), '; expires='.concat(UtilsCookie.calculateExpiration(that.options.cookieExpire)), that.options.cookiePath ? '; path='.concat(that.options.cookiePath) : '', that.options.cookieDomain ? '; domain='.concat(that.options.cookieDomain) : '', that.options.cookieSecure ? '; secure' : '', ';SameSite='.concat(that.options.cookieSameSite)].join('')
          break

        case 'localStorage':
          localStorage.setItem(cookieName, cookieValue)
          break

        case 'sessionStorage':
          sessionStorage.setItem(cookieName, cookieValue)
          break

        case 'customStorage':
          if (!that.options.cookieCustomStorageSet || !that.options.cookieCustomStorageGet || !that.options.cookieCustomStorageDelete) {
            throw new Error('The following options must be set while using the customStorage: cookieCustomStorageSet, cookieCustomStorageGet and cookieCustomStorageDelete')
          }

          Utils.calculateObjectValue(that.options, that.options.cookieCustomStorageSet, [cookieName, cookieValue], '')
          break

        default:
          return false
      }

      return true
    },
    getCookie: function getCookie (that, tableName, cookieName) {
      if (!cookieName) {
        return null
      }

      if (UtilsCookie.inArrayCookiesEnabled(cookieName, that.options.cookiesEnabled) === -1) {
        return null
      }

      cookieName = ''.concat(tableName, '.').concat(cookieName)

      switch (that.options.cookieStorage) {
        case 'cookieStorage':
          var value = '; '.concat(document.cookie)
          var parts = value.split('; '.concat(cookieName, '='))
          return parts.length === 2 ? decodeURIComponent(parts.pop().split(';').shift()) : null

        case 'localStorage':
          return localStorage.getItem(cookieName)

        case 'sessionStorage':
          return sessionStorage.getItem(cookieName)

        case 'customStorage':
          if (!that.options.cookieCustomStorageSet || !that.options.cookieCustomStorageGet || !that.options.cookieCustomStorageDelete) {
            throw new Error('The following options must be set while using the customStorage: cookieCustomStorageSet, cookieCustomStorageGet and cookieCustomStorageDelete')
          }

          return Utils.calculateObjectValue(that.options, that.options.cookieCustomStorageGet, [cookieName], '')

        default:
          return null
      }
    },
    deleteCookie: function deleteCookie (that, tableName, cookieName) {
      cookieName = ''.concat(tableName, '.').concat(cookieName)

      switch (that.options.cookieStorage) {
        case 'cookieStorage':
          document.cookie = [encodeURIComponent(cookieName), '=', '; expires=Thu, 01 Jan 1970 00:00:00 GMT', that.options.cookiePath ? '; path='.concat(that.options.cookiePath) : '', that.options.cookieDomain ? '; domain='.concat(that.options.cookieDomain) : '', ';SameSite='.concat(that.options.cookieSameSite)].join('')
          break

        case 'localStorage':
          localStorage.removeItem(cookieName)
          break

        case 'sessionStorage':
          sessionStorage.removeItem(cookieName)
          break

        case 'customStorage':
          if (!that.options.cookieCustomStorageSet || !that.options.cookieCustomStorageGet || !that.options.cookieCustomStorageDelete) {
            throw new Error('The following options must be set while using the customStorage: cookieCustomStorageSet, cookieCustomStorageGet and cookieCustomStorageDelete')
          }

          Utils.calculateObjectValue(that.options, that.options.cookieCustomStorageDelete, [cookieName], '')
          break

        default:
          return false
      }

      return true
    },
    calculateExpiration: function calculateExpiration (cookieExpire) {
      const time = cookieExpire.replace(/[0-9]*/, '') // s,mi,h,d,m,y

      cookieExpire = cookieExpire.replace(/[A-Za-z]{1,2}/, '') // number

      switch (time.toLowerCase()) {
        case 's':
          cookieExpire = +cookieExpire
          break

        case 'mi':
          cookieExpire *= 60
          break

        case 'h':
          cookieExpire = cookieExpire * 60 * 60
          break

        case 'd':
          cookieExpire = cookieExpire * 24 * 60 * 60
          break

        case 'm':
          cookieExpire = cookieExpire * 30 * 24 * 60 * 60
          break

        case 'y':
          cookieExpire = cookieExpire * 365 * 24 * 60 * 60
          break

        default:
          cookieExpire = undefined
          break
      }

      if (!cookieExpire) {
        return ''
      }

      const d = new Date()
      d.setTime(d.getTime() + cookieExpire * 1000)
      return d.toGMTString()
    },
    initCookieFilters: function initCookieFilters (bootstrapTable) {
      setTimeout(function () {
        const parsedCookieFilters = JSON.parse(UtilsCookie.getCookie(bootstrapTable, bootstrapTable.options.cookieIdTable, UtilsCookie.cookieIds.filterControl))

        if (!bootstrapTable.options.filterControlValuesLoaded && parsedCookieFilters) {
          const cachedFilters = {}
          const header = UtilsCookie.getCurrentHeader(bootstrapTable)
          const searchControls = UtilsCookie.getCurrentSearchControls(bootstrapTable)

          const applyCookieFilters = function applyCookieFilters (element, filteredCookies) {
            filteredCookies.forEach(function (cookie) {
              if (cookie.text === '' || element.type === 'radio' && element.value.toString() !== cookie.text.toString()) {
                return
              }

              if (element.tagName === 'INPUT' && element.type === 'radio' && element.value.toString() === cookie.text.toString()) {
                element.checked = true
                cachedFilters[cookie.field] = cookie.text
              } else if (element.tagName === 'INPUT') {
                element.value = cookie.text
                cachedFilters[cookie.field] = cookie.text
              } else if (element.tagName === 'SELECT' && bootstrapTable.options.filterControlContainer) {
                element.value = cookie.text
                cachedFilters[cookie.field] = cookie.text
              } else if (cookie.text !== '' && element.tagName === 'SELECT') {
                for (let i = 0; i < element.length; i++) {
                  const currentElement = element[i]

                  if (currentElement.value === cookie.text) {
                    currentElement.selected = true
                    return
                  }
                }

                const option = document.createElement('option')
                option.value = cookie.text
                option.text = cookie.text
                element.add(option, element[1])
                element.selectedIndex = 1
                cachedFilters[cookie.field] = cookie.text
              }
            })
          }

          let filterContainer = header

          if (bootstrapTable.options.filterControlContainer) {
            filterContainer = $__default.default(''.concat(bootstrapTable.options.filterControlContainer))
          }

          filterContainer.find(searchControls).each(function () {
            const field = $__default.default(this).closest('[data-field]').data('field')
            const filteredCookies = parsedCookieFilters.filter(function (cookie) {
              return cookie.field === field
            })
            applyCookieFilters(this, filteredCookies)
          })
          bootstrapTable.initColumnSearch(cachedFilters)
          bootstrapTable.options.filterControlValuesLoaded = true
          bootstrapTable.initServer()
        }
      }, 250)
    }
  }
  $__default.default.extend($__default.default.fn.bootstrapTable.defaults, {
    cookie: false,
    cookieExpire: '2h',
    cookiePath: null,
    cookieDomain: null,
    cookieSecure: null,
    cookieSameSite: 'Lax',
    cookieIdTable: '',
    cookiesEnabled: ['bs.table.sortOrder', 'bs.table.sortName', 'bs.table.pageNumber', 'bs.table.pageList', 'bs.table.columns', 'bs.table.searchText', 'bs.table.filterControl', 'bs.table.filterBy', 'bs.table.reorderColumns'],
    cookieStorage: 'cookieStorage',
    // localStorage, sessionStorage, customStorage
    cookieCustomStorageGet: null,
    cookieCustomStorageSet: null,
    cookieCustomStorageDelete: null,
    // internal variable
    filterControls: [],
    filterControlValuesLoaded: false
  })
  $__default.default.fn.bootstrapTable.methods.push('getCookies')
  $__default.default.fn.bootstrapTable.methods.push('deleteCookie')
  $__default.default.extend($__default.default.fn.bootstrapTable.utils, {
    setCookie: UtilsCookie.setCookie,
    getCookie: UtilsCookie.getCookie
  })

  $__default.default.BootstrapTable = /* #__PURE__ */(function (_$$BootstrapTable) {
    _inherits(_class, _$$BootstrapTable)

    const _super = _createSuper(_class)

    function _class () {
      _classCallCheck(this, _class)

      return _super.apply(this, arguments)
    }

    _createClass(_class, [{
      key: 'init',
      value: function init () {
        if (this.options.cookie) {
          // FilterBy logic
          const filterByCookieValue = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.filterBy)

          if (typeof filterByCookieValue === 'boolean' && !filterByCookieValue) {
            throw new Error('The cookie value of filterBy must be a json!')
          }

          let filterByCookie = {}

          try {
            filterByCookie = JSON.parse(filterByCookieValue)
          } catch (e) {
            throw new Error('Could not parse the json of the filterBy cookie!')
          }

          this.filterColumns = filterByCookie || {} // FilterControl logic

          this.options.filterControls = []
          this.options.filterControlValuesLoaded = false
          this.options.cookiesEnabled = typeof this.options.cookiesEnabled === 'string' ? this.options.cookiesEnabled.replace('[', '').replace(']', '').replace(/'/g, '').replace(/ /g, '').toLowerCase().split(',') : this.options.cookiesEnabled

          if (this.options.filterControl) {
            const that = this
            this.$el.on('column-search.bs.table', function (e, field, text) {
              let isNewField = true

              for (let i = 0; i < that.options.filterControls.length; i++) {
                if (that.options.filterControls[i].field === field) {
                  that.options.filterControls[i].text = text
                  isNewField = false
                  break
                }
              }

              if (isNewField) {
                that.options.filterControls.push({
                  field: field,
                  text: text
                })
              }

              UtilsCookie.setCookie(that, UtilsCookie.cookieIds.filterControl, JSON.stringify(that.options.filterControls))
            }).on('created-controls.bs.table', UtilsCookie.initCookieFilters(that))
          }
        }

        _get(_getPrototypeOf(_class.prototype), 'init', this).call(this)
      }
    }, {
      key: 'initServer',
      value: function initServer () {
        let _get2

        if (this.options.cookie && this.options.filterControl && !this.options.filterControlValuesLoaded) {
          const cookie = JSON.parse(UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.filterControl))

          if (cookie) {
            return
          }
        }

        for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
          args[_key] = arguments[_key]
        }

        (_get2 = _get(_getPrototypeOf(_class.prototype), 'initServer', this)).call.apply(_get2, [this].concat(args))
      }
    }, {
      key: 'initTable',
      value: function initTable () {
        let _get3

        for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
          args[_key2] = arguments[_key2]
        }

        (_get3 = _get(_getPrototypeOf(_class.prototype), 'initTable', this)).call.apply(_get3, [this].concat(args))

        this.initCookie()
      }
    }, {
      key: 'onSort',
      value: function onSort () {
        let _get4

        for (var _len3 = arguments.length, args = new Array(_len3), _key3 = 0; _key3 < _len3; _key3++) {
          args[_key3] = arguments[_key3]
        }

        (_get4 = _get(_getPrototypeOf(_class.prototype), 'onSort', this)).call.apply(_get4, [this].concat(args))

        if (this.options.sortName === undefined || this.options.sortOrder === undefined) {
          UtilsCookie.deleteCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.sortName)
          UtilsCookie.deleteCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.sortOrder)
          return
        }

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.sortOrder, this.options.sortOrder)
        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.sortName, this.options.sortName)
      }
    }, {
      key: 'onPageNumber',
      value: function onPageNumber () {
        let _get5

        for (var _len4 = arguments.length, args = new Array(_len4), _key4 = 0; _key4 < _len4; _key4++) {
          args[_key4] = arguments[_key4]
        }

        (_get5 = _get(_getPrototypeOf(_class.prototype), 'onPageNumber', this)).call.apply(_get5, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageNumber, this.options.pageNumber)
      }
    }, {
      key: 'onPageListChange',
      value: function onPageListChange () {
        let _get6

        for (var _len5 = arguments.length, args = new Array(_len5), _key5 = 0; _key5 < _len5; _key5++) {
          args[_key5] = arguments[_key5]
        }

        (_get6 = _get(_getPrototypeOf(_class.prototype), 'onPageListChange', this)).call.apply(_get6, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageList, this.options.pageSize)
        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageNumber, this.options.pageNumber)
      }
    }, {
      key: 'onPagePre',
      value: function onPagePre () {
        let _get7

        for (var _len6 = arguments.length, args = new Array(_len6), _key6 = 0; _key6 < _len6; _key6++) {
          args[_key6] = arguments[_key6]
        }

        (_get7 = _get(_getPrototypeOf(_class.prototype), 'onPagePre', this)).call.apply(_get7, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageNumber, this.options.pageNumber)
      }
    }, {
      key: 'onPageNext',
      value: function onPageNext () {
        let _get8

        for (var _len7 = arguments.length, args = new Array(_len7), _key7 = 0; _key7 < _len7; _key7++) {
          args[_key7] = arguments[_key7]
        }

        (_get8 = _get(_getPrototypeOf(_class.prototype), 'onPageNext', this)).call.apply(_get8, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageNumber, this.options.pageNumber)
      }
    }, {
      key: '_toggleColumn',
      value: function _toggleColumn () {
        let _get9

        for (var _len8 = arguments.length, args = new Array(_len8), _key8 = 0; _key8 < _len8; _key8++) {
          args[_key8] = arguments[_key8]
        }

        (_get9 = _get(_getPrototypeOf(_class.prototype), '_toggleColumn', this)).call.apply(_get9, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.columns, JSON.stringify(this.getVisibleColumns().map(function (column) {
          return column.field
        })))
      }
    }, {
      key: '_toggleAllColumns',
      value: function _toggleAllColumns () {
        let _get10

        for (var _len9 = arguments.length, args = new Array(_len9), _key9 = 0; _key9 < _len9; _key9++) {
          args[_key9] = arguments[_key9]
        }

        (_get10 = _get(_getPrototypeOf(_class.prototype), '_toggleAllColumns', this)).call.apply(_get10, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.columns, JSON.stringify(this.getVisibleColumns().map(function (column) {
          return column.field
        })))
      }
    }, {
      key: 'selectPage',
      value: function selectPage (page) {
        _get(_getPrototypeOf(_class.prototype), 'selectPage', this).call(this, page)

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageNumber, page)
      }
    }, {
      key: 'onSearch',
      value: function onSearch (event) {
        _get(_getPrototypeOf(_class.prototype), 'onSearch', this).call(this, event)

        if (this.options.search) {
          UtilsCookie.setCookie(this, UtilsCookie.cookieIds.searchText, this.searchText)
        }

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.pageNumber, this.options.pageNumber)
      }
    }, {
      key: 'initHeader',
      value: function initHeader () {
        let _get11

        if (this.options.reorderableColumns) {
          this.columnsSortOrder = JSON.parse(UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.reorderColumns))
        }

        for (var _len10 = arguments.length, args = new Array(_len10), _key10 = 0; _key10 < _len10; _key10++) {
          args[_key10] = arguments[_key10]
        }

        (_get11 = _get(_getPrototypeOf(_class.prototype), 'initHeader', this)).call.apply(_get11, [this].concat(args))
      }
    }, {
      key: 'persistReorderColumnsState',
      value: function persistReorderColumnsState (that) {
        UtilsCookie.setCookie(that, UtilsCookie.cookieIds.reorderColumns, JSON.stringify(that.columnsSortOrder))
      }
    }, {
      key: 'filterBy',
      value: function filterBy () {
        let _get12

        for (var _len11 = arguments.length, args = new Array(_len11), _key11 = 0; _key11 < _len11; _key11++) {
          args[_key11] = arguments[_key11]
        }

        (_get12 = _get(_getPrototypeOf(_class.prototype), 'filterBy', this)).call.apply(_get12, [this].concat(args))

        UtilsCookie.setCookie(this, UtilsCookie.cookieIds.filterBy, JSON.stringify(this.filterColumns))
      }
    }, {
      key: 'initCookie',
      value: function initCookie () {
        const _this = this

        if (!this.options.cookie) {
          return
        }

        if (this.options.cookieIdTable === '' || this.options.cookieExpire === '' || !UtilsCookie.cookieEnabled()) {
          console.error('Configuration error. Please review the cookieIdTable and the cookieExpire property. If the properties are correct, then this browser does not support cookies.')
          this.options.cookie = false // Make sure that the cookie extension is disabled

          return
        }

        const sortOrderCookie = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.sortOrder)
        const sortOrderNameCookie = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.sortName)
        const pageNumberCookie = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.pageNumber)
        const pageListCookie = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.pageList)
        const searchTextCookie = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.searchText)
        const columnsCookieValue = UtilsCookie.getCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds.columns)

        if (typeof columnsCookieValue === 'boolean' && !columnsCookieValue) {
          throw new Error('The cookie value of filterBy must be a json!')
        }

        let columnsCookie = {}

        try {
          columnsCookie = JSON.parse(columnsCookieValue)
        } catch (e) {
          throw new Error('Could not parse the json of the columns cookie!', columnsCookieValue)
        } // sortOrder

        this.options.sortOrder = sortOrderCookie || this.options.sortOrder // sortName

        this.options.sortName = sortOrderNameCookie || this.options.sortName // pageNumber

        this.options.pageNumber = pageNumberCookie ? +pageNumberCookie : this.options.pageNumber // pageSize

        this.options.pageSize = pageListCookie ? pageListCookie === this.options.formatAllRows() ? pageListCookie : +pageListCookie : this.options.pageSize // searchText

        this.options.searchText = searchTextCookie || ''

        if (columnsCookie) {
          const _iterator = _createForOfIteratorHelper(this.columns)
          let _step

          try {
            const _loop = function _loop () {
              const column = _step.value
              column.visible = columnsCookie.filter(function (columnField) {
                if (_this.isSelectionColumn(column)) {
                  return true
                }
                /**
                 * This is needed for the old saved cookies or the table will show no columns!
                 * It can be removed in 2-3 Versions Later!!
                 * TODO: Remove this part some versions later e.g. 1.17.3
                 */

                if (columnField instanceof Object) {
                  return columnField.field === column.field
                }

                return columnField === column.field
              }).length > 0 || !column.switchable
            }

            for (_iterator.s(); !(_step = _iterator.n()).done;) {
              _loop()
            }
          } catch (err) {
            _iterator.e(err)
          } finally {
            _iterator.f()
          }
        }
      }
    }, {
      key: 'getCookies',
      value: function getCookies () {
        const bootstrapTable = this
        const cookies = {}
        $__default.default.each(UtilsCookie.cookieIds, function (key, value) {
          cookies[key] = UtilsCookie.getCookie(bootstrapTable, bootstrapTable.options.cookieIdTable, value)

          if (key === 'columns') {
            cookies[key] = JSON.parse(cookies[key])
          }
        })
        return cookies
      }
    }, {
      key: 'deleteCookie',
      value: function deleteCookie (cookieName) {
        if (cookieName === '' || !UtilsCookie.cookieEnabled()) {
          return
        }

        UtilsCookie.deleteCookie(this, this.options.cookieIdTable, UtilsCookie.cookieIds[cookieName])
      }
    }])

    return _class
  }($__default.default.BootstrapTable))
}))
