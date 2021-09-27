(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('jquery'))
    : typeof define === 'function' && define.amd ? define(['exports', 'jquery'], factory)
      : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.BootstrapTable = {}, global.jQuery))
}(this, function (exports, $) {
  'use strict'

  function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { default: e } }

  const $__default = /* #__PURE__ */_interopDefaultLegacy($)

  function _typeof (obj) {
    '@babel/helpers - typeof'

    if (typeof Symbol === 'function' && typeof Symbol.iterator === 'symbol') {
      _typeof = function (obj) {
        return typeof obj
      }
    } else {
      _typeof = function (obj) {
        return obj && typeof Symbol === 'function' && obj.constructor === Symbol && obj !== Symbol.prototype ? 'symbol' : typeof obj
      }
    }

    return _typeof(obj)
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

  const push = [].push

  // `Array.prototype.{ forEach, map, filter, some, every, find, findIndex, filterOut }` methods implementation
  const createMethod$2 = function (TYPE) {
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
    forEach: createMethod$2(0),
    // `Array.prototype.map` method
    // https://tc39.es/ecma262/#sec-array.prototype.map
    map: createMethod$2(1),
    // `Array.prototype.filter` method
    // https://tc39.es/ecma262/#sec-array.prototype.filter
    filter: createMethod$2(2),
    // `Array.prototype.some` method
    // https://tc39.es/ecma262/#sec-array.prototype.some
    some: createMethod$2(3),
    // `Array.prototype.every` method
    // https://tc39.es/ecma262/#sec-array.prototype.every
    every: createMethod$2(4),
    // `Array.prototype.find` method
    // https://tc39.es/ecma262/#sec-array.prototype.find
    find: createMethod$2(5),
    // `Array.prototype.findIndex` method
    // https://tc39.es/ecma262/#sec-array.prototype.findIndex
    findIndex: createMethod$2(6),
    // `Array.prototype.filterOut` method
    // https://github.com/tc39/proposal-array-filtering
    filterOut: createMethod$2(7)
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

  const TO_STRING_TAG$1 = wellKnownSymbol('toStringTag')
  const test$1 = {}

  test$1[TO_STRING_TAG$1] = 'z'

  const toStringTagSupport = String(test$1) === '[object z]'

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

  // a string of all valid unicode whitespaces
  const whitespaces = '\u0009\u000A\u000B\u000C\u000D\u0020\u00A0\u1680\u2000\u2001\u2002' +
    '\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u2028\u2029\uFEFF'

  const whitespace = '[' + whitespaces + ']'
  const ltrim = RegExp('^' + whitespace + whitespace + '*')
  const rtrim = RegExp(whitespace + whitespace + '*$')

  // `String.prototype.{ trim, trimStart, trimEnd, trimLeft, trimRight }` methods implementation
  const createMethod$1 = function (TYPE) {
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
    start: createMethod$1(1),
    // `String.prototype.{ trimRight, trimEnd }` methods
    // https://tc39.es/ecma262/#sec-string.prototype.trimend
    end: createMethod$1(2),
    // `String.prototype.trim` method
    // https://tc39.es/ecma262/#sec-string.prototype.trim
    trim: createMethod$1(3)
  }

  const non = '\u200B\u0085\u180E'

  // check that a method works with the correct list
  // of whitespaces and has a correct name
  const stringTrimForced = function (METHOD_NAME) {
    return fails(function () {
      return !!whitespaces[METHOD_NAME]() || non[METHOD_NAME]() != non || whitespaces[METHOD_NAME].name !== METHOD_NAME
    })
  }

  const $trim = stringTrim.trim

  // `String.prototype.trim` method
  // https://tc39.es/ecma262/#sec-string.prototype.trim
  _export({ target: 'String', proto: true, forced: stringTrimForced('trim') }, {
    trim: function trim () {
      return $trim(this)
    }
  })

  const createProperty = function (object, key, value) {
    const propertyKey = toPrimitive(key)
    if (propertyKey in object) objectDefineProperty.f(object, propertyKey, createPropertyDescriptor(0, value))
    else object[propertyKey] = value
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

  const FORCED$1 = !IS_CONCAT_SPREADABLE_SUPPORT || !SPECIES_SUPPORT

  // `Array.prototype.concat` method
  // https://tc39.es/ecma262/#sec-array.prototype.concat
  // with adding support of @@isConcatSpreadable and @@species
  _export({ target: 'Array', proto: true, forced: FORCED$1 }, {
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

  const test = []
  const nativeSort = test.sort

  // IE8-
  const FAILS_ON_UNDEFINED = fails(function () {
    test.sort(undefined)
  })
  // V8 bug
  const FAILS_ON_NULL = fails(function () {
    test.sort(null)
  })
  // Old WebKit
  const STRICT_METHOD$3 = arrayMethodIsStrict('sort')

  const FORCED = FAILS_ON_UNDEFINED || !FAILS_ON_NULL || !STRICT_METHOD$3

  // `Array.prototype.sort` method
  // https://tc39.es/ecma262/#sec-array.prototype.sort
  _export({ target: 'Array', proto: true, forced: FORCED }, {
    sort: function sort (comparefn) {
      return comparefn === undefined
        ? nativeSort.call(toObject(this))
        : nativeSort.call(toObject(this), aFunction(comparefn))
    }
  })

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

  // `String.prototype.{ codePointAt, at }` methods implementation
  const createMethod = function (CONVERT_TO_STRING) {
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
    codeAt: createMethod(false),
    // `String.prototype.at` method
    // https://github.com/mathiasbynens/String.prototype.at
    charAt: createMethod(true)
  }

  const charAt = stringMultibyte.charAt

  // `AdvanceStringIndex` abstract operation
  // https://tc39.es/ecma262/#sec-advancestringindex
  const advanceStringIndex = function (S, index, unicode) {
    return index + (unicode ? charAt(S, index).length : 1)
  }

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

  const max = Math.max
  const min$1 = Math.min

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
          const position = max(min$1(toInteger(result.index), S.length), 0)
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

  // @@match logic
  fixRegexpWellKnownSymbolLogic('match', 1, function (MATCH, nativeMatch, maybeCallNative) {
    return [
      // `String.prototype.match` method
      // https://tc39.es/ecma262/#sec-string.prototype.match
      function match (regexp) {
        const O = requireObjectCoercible(this)
        const matcher = regexp == undefined ? undefined : regexp[MATCH]
        return matcher !== undefined ? matcher.call(regexp, O) : new RegExp(regexp)[MATCH](String(O))
      },
      // `RegExp.prototype[@@match]` method
      // https://tc39.es/ecma262/#sec-regexp.prototype-@@match
      function (regexp) {
        const res = maybeCallNative(nativeMatch, regexp, this)
        if (res.done) return res.value

        const rx = anObject(regexp)
        const S = String(this)

        if (!rx.global) return regexpExecAbstract(rx, S)

        const fullUnicode = rx.unicode
        rx.lastIndex = 0
        const A = []
        let n = 0
        let result
        while ((result = regexpExecAbstract(rx, S)) !== null) {
          const matchStr = String(result[0])
          A[n] = matchStr
          if (matchStr === '') rx.lastIndex = advanceStringIndex(S, toLength(rx.lastIndex), fullUnicode)
          n++
        }
        return n === 0 ? null : A
      }
    ]
  })

  const MATCH = wellKnownSymbol('match')

  // `IsRegExp` abstract operation
  // https://tc39.es/ecma262/#sec-isregexp
  const isRegexp = function (it) {
    let isRegExp
    return isObject(it) && ((isRegExp = it[MATCH]) !== undefined ? !!isRegExp : classofRaw(it) == 'RegExp')
  }

  const SPECIES = wellKnownSymbol('species')

  // `SpeciesConstructor` abstract operation
  // https://tc39.es/ecma262/#sec-speciesconstructor
  const speciesConstructor = function (O, defaultConstructor) {
    const C = anObject(O).constructor
    let S
    return C === undefined || (S = anObject(C)[SPECIES]) == undefined ? defaultConstructor : aFunction(S)
  }

  const arrayPush = [].push
  const min = Math.min
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
            (e = min(toLength(splitter.lastIndex + (SUPPORTS_Y ? 0 : q)), S.length)) === p
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

  const $includes = arrayIncludes.includes

  // `Array.prototype.includes` method
  // https://tc39.es/ecma262/#sec-array.prototype.includes
  _export({ target: 'Array', proto: true }, {
    includes: function includes (el /* , fromIndex = 0 */) {
      return $includes(this, el, arguments.length > 1 ? arguments[1] : undefined)
    }
  })

  // https://tc39.es/ecma262/#sec-array.prototype-@@unscopables
  addToUnscopables('includes')

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

  const $forEach = arrayIteration.forEach

  const STRICT_METHOD$2 = arrayMethodIsStrict('forEach')

  // `Array.prototype.forEach` method implementation
  // https://tc39.es/ecma262/#sec-array.prototype.foreach
  const arrayForEach = !STRICT_METHOD$2 ? function forEach (callbackfn /* , thisArg */) {
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

  const FAILS_ON_PRIMITIVES = fails(function () { objectKeys(1) })

  // `Object.keys` method
  // https://tc39.es/ecma262/#sec-object.keys
  _export({ target: 'Object', stat: true, forced: FAILS_ON_PRIMITIVES }, {
    keys: function keys (it) {
      return objectKeys(toObject(it))
    }
  })

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

  const $indexOf = arrayIncludes.indexOf

  const nativeIndexOf = [].indexOf

  const NEGATIVE_ZERO = !!nativeIndexOf && 1 / [1].indexOf(1, -0) < 0
  const STRICT_METHOD = arrayMethodIsStrict('indexOf')

  // `Array.prototype.indexOf` method
  // https://tc39.es/ecma262/#sec-array.prototype.indexof
  _export({ target: 'Array', proto: true, forced: NEGATIVE_ZERO || !STRICT_METHOD }, {
    indexOf: function indexOf (searchElement /* , fromIndex = 0 */) {
      return NEGATIVE_ZERO
        // convert -0 to +0
        ? nativeIndexOf.apply(this, arguments) || 0
        : $indexOf(this, searchElement, arguments.length > 1 ? arguments[1] : undefined)
    }
  })

  const Utils = $__default.default.fn.bootstrapTable.utils
  const searchControls = 'select, input:not([type="checkbox"]):not([type="radio"])'
  function getOptionsFromSelectControl (selectControl) {
    return selectControl.get(selectControl.length - 1).options
  }
  function getControlContainer (that) {
    if (that.options.filterControlContainer) {
      return $__default.default(''.concat(that.options.filterControlContainer))
    }

    return that.$header
  }
  function getSearchControls (that) {
    return getControlContainer(that).find(searchControls)
  }
  function hideUnusedSelectOptions (selectControl, uniqueValues) {
    const options = getOptionsFromSelectControl(selectControl)

    for (let i = 0; i < options.length; i++) {
      if (options[i].value !== '') {
        if (!uniqueValues.hasOwnProperty(options[i].value)) {
          selectControl.find(Utils.sprintf('option[value=\'%s\']', options[i].value)).hide()
        } else {
          selectControl.find(Utils.sprintf('option[value=\'%s\']', options[i].value)).show()
        }
      }
    }
  }
  function existOptionInSelectControl (selectControl, value) {
    const options = getOptionsFromSelectControl(selectControl)

    for (let i = 0; i < options.length; i++) {
      if (options[i].value === Utils.unescapeHTML(value.toString())) {
        // The value is not valid to add
        return true
      }
    } // If we get here, the value is valid to add

    return false
  }
  function addOptionToSelectControl (selectControl, _value, text, selected) {
    const value = _value === undefined || _value === null ? '' : _value.toString().trim()
    const $selectControl = $__default.default(selectControl.get(selectControl.length - 1))

    if (!existOptionInSelectControl(selectControl, value)) {
      const option = $__default.default('<option value="'.concat(value, '">').concat(text, '</option>'))

      if (value === selected) {
        option.attr('selected', true)
      }

      $selectControl.append(option)
    }
  }
  function sortSelectControl (selectControl, orderBy) {
    const $selectControl = $__default.default(selectControl.get(selectControl.length - 1))
    const $opts = $selectControl.find('option:gt(0)')

    if (orderBy !== 'server') {
      $opts.sort(function (a, b) {
        return Utils.sort(a.textContent, b.textContent, orderBy === 'desc' ? -1 : 1)
      })
    }

    $selectControl.find('option:gt(0)').remove()
    $selectControl.append($opts)
  }
  function fixHeaderCSS (_ref) {
    const $tableHeader = _ref.$tableHeader
    $tableHeader.css('height', '89px')
  }
  function getElementClass ($element) {
    return $element.attr('class').replace('form-control', '').replace('focus-temp', '').replace('search-input', '').trim()
  }
  function getCursorPosition (el) {
    if (Utils.isIEBrowser()) {
      if ($__default.default(el).is('input[type=text]')) {
        let pos = 0

        if ('selectionStart' in el) {
          pos = el.selectionStart
        } else if ('selection' in document) {
          el.focus()
          const Sel = document.selection.createRange()
          const SelLength = document.selection.createRange().text.length
          Sel.moveStart('character', -el.value.length)
          pos = Sel.text.length - SelLength
        }

        return pos
      }

      return -1
    }

    return -1
  }
  function setCursorPosition (el) {
    $__default.default(el).val(el.value)
  }
  function copyValues (that) {
    const searchControls = getSearchControls(that)
    that.options.valuesFilterControl = []
    searchControls.each(function () {
      let $field = $__default.default(this)

      if (that.options.height) {
        const fieldClass = getElementClass($field)
        $field = $__default.default('.fixed-table-header .'.concat(fieldClass))
      }

      that.options.valuesFilterControl.push({
        field: $field.closest('[data-field]').data('field'),
        value: $field.val(),
        position: getCursorPosition($field.get(0)),
        hasFocus: $field.is(':focus')
      })
    })
  }
  function setValues (that) {
    let field = null
    let result = []
    const searchControls = getSearchControls(that)

    if (that.options.valuesFilterControl.length > 0) {
      //  Callback to apply after settings fields values
      let fieldToFocusCallback = null
      searchControls.each(function (i, el) {
        const $this = $__default.default(el)
        field = $this.closest('[data-field]').data('field')
        result = that.options.valuesFilterControl.filter(function (valueObj) {
          return valueObj.field === field
        })

        if (result.length > 0) {
          if ($this.is('[type=radio]')) {
            return
          }

          $this.val(result[0].value)

          if (result[0].hasFocus && result[0].value !== '') {
            // set callback if the field had the focus.
            fieldToFocusCallback = (function (fieldToFocus, carretPosition) {
              // Closure here to capture the field and cursor position
              const closedCallback = function closedCallback () {
                fieldToFocus.focus()
                setCursorPosition(fieldToFocus)
              }

              return closedCallback
            }($this.get(0), result[0].position))
          }
        }
      }) // Callback call.

      if (fieldToFocusCallback !== null) {
        fieldToFocusCallback()
      }
    }
  }
  function collectBootstrapCookies () {
    const cookies = []
    const foundCookies = document.cookie.match(/(?:bs.table.)(\w*)/g)
    const foundLocalStorage = localStorage

    if (foundCookies) {
      $__default.default.each(foundCookies, function (i, _cookie) {
        let cookie = _cookie

        if (/./.test(cookie)) {
          cookie = cookie.split('.').pop()
        }

        if ($__default.default.inArray(cookie, cookies) === -1) {
          cookies.push(cookie)
        }
      })
    }

    if (foundLocalStorage) {
      for (let i = 0; i < foundLocalStorage.length; i++) {
        let cookie = foundLocalStorage.key(i)

        if (/./.test(cookie)) {
          cookie = cookie.split('.').pop()
        }

        if (!cookies.includes(cookie)) {
          cookies.push(cookie)
        }
      }
    }

    return cookies
  }
  function escapeID (id) {
    // eslint-disable-next-line no-useless-escape
    return String(id).replace(/([:.\[\],])/g, '\\$1')
  }
  function isColumnSearchableViaSelect (_ref2) {
    const filterControl = _ref2.filterControl
    const searchable = _ref2.searchable
    return filterControl && filterControl.toLowerCase() === 'select' && searchable
  }
  function isFilterDataNotGiven (_ref3) {
    const filterData = _ref3.filterData
    return filterData === undefined || filterData.toLowerCase() === 'column'
  }
  function hasSelectControlElement (selectControl) {
    return selectControl && selectControl.length > 0
  }
  function initFilterSelectControls (that) {
    const data = that.data
    const z = that.options.pagination ? that.options.sidePagination === 'server' ? that.pageTo : that.options.totalRows : that.pageTo
    $__default.default.each(that.header.fields, function (j, field) {
      const column = that.columns[that.fieldsColumnsIndex[field]]
      const selectControl = getControlContainer(that).find('select.bootstrap-table-filter-control-'.concat(escapeID(column.field)))

      if (isColumnSearchableViaSelect(column) && isFilterDataNotGiven(column) && hasSelectControlElement(selectControl)) {
        if (selectControl.get(selectControl.length - 1).options.length === 0) {
          // Added the default option, must use a non-breaking space(&nbsp;) to pass the W3C validator
          addOptionToSelectControl(selectControl, '', column.filterControlPlaceholder || '&nbsp;', column.filterDefault)
        }

        const uniqueValues = {}

        for (let i = 0; i < z; i++) {
          // Added a new value
          let fieldValue = Utils.getItemField(data[i], field, false)
          const formatter = that.options.editable && column.editable ? column._formatter : that.header.formatters[j]
          let formattedValue = Utils.calculateObjectValue(that.header, formatter, [fieldValue, data[i], i], fieldValue)

          if (column.filterDataCollector) {
            formattedValue = Utils.calculateObjectValue(that.header, column.filterDataCollector, [fieldValue, data[i], formattedValue], formattedValue)
          }

          if (column.searchFormatter) {
            fieldValue = formattedValue
          }

          uniqueValues[formattedValue] = fieldValue

          if (_typeof(formattedValue) === 'object' && formattedValue !== null) {
            formattedValue.forEach(function (value) {
              addOptionToSelectControl(selectControl, value, value, column.filterDefault)
            })
            continue
          } // eslint-disable-next-line guard-for-in

          for (const key in uniqueValues) {
            addOptionToSelectControl(selectControl, uniqueValues[key], key, column.filterDefault)
          }
        }

        sortSelectControl(selectControl, column.filterOrderBy)

        if (that.options.hideUnusedSelectOptions) {
          hideUnusedSelectOptions(selectControl, uniqueValues)
        }
      }
    })
  }
  function getFilterDataMethod (objFilterDataMethod, searchTerm) {
    const keys = Object.keys(objFilterDataMethod)

    for (let i = 0; i < keys.length; i++) {
      if (keys[i] === searchTerm) {
        return objFilterDataMethod[searchTerm]
      }
    }

    return null
  }
  function createControls (that, header) {
    let addedFilterControl = false
    let html
    $__default.default.each(that.columns, function (_, column) {
      html = []

      if (!column.visible) {
        return
      }

      if (!column.filterControl && !that.options.filterControlContainer) {
        html.push('<div class="no-filter-control"></div>')
      } else if (that.options.filterControlContainer) {
        const $filterControls = $__default.default('.bootstrap-table-filter-control-'.concat(column.field))
        $__default.default.each($filterControls, function (_, filterControl) {
          const $filterControl = $__default.default(filterControl)

          if (!$filterControl.is('[type=radio]')) {
            const placeholder = column.filterControlPlaceholder ? column.filterControlPlaceholder : ''
            $filterControl.attr('placeholder', placeholder).val(column.filterDefault)
          }

          $filterControl.attr('data-field', column.field)
        })
        addedFilterControl = true
      } else {
        const nameControl = column.filterControl.toLowerCase()
        html.push('<div class="filter-control">')
        addedFilterControl = true

        if (column.searchable && that.options.filterTemplate[nameControl]) {
          html.push(that.options.filterTemplate[nameControl](that, column.field, column.filterControlPlaceholder ? column.filterControlPlaceholder : '', column.filterDefault))
        }
      }

      if (!column.filterControl && column.filterDefault !== '' && typeof column.filterDefault !== 'undefined') {
        if ($__default.default.isEmptyObject(that.filterColumnsPartial)) {
          that.filterColumnsPartial = {}
        }

        that.filterColumnsPartial[column.field] = column.filterDefault
      }

      $__default.default.each(header.find('th'), function (i, th) {
        const $th = $__default.default(th)

        if ($th.data('field') === column.field) {
          $th.find('.fht-cell').append(html.join(''))
          return false
        }
      })

      if (column.filterData && column.filterData.toLowerCase() !== 'column') {
        const filterDataType = getFilterDataMethod(
        /* eslint-disable no-use-before-define */
          filterDataMethods, column.filterData.substring(0, column.filterData.indexOf(':')))
        let filterDataSource
        let selectControl

        if (filterDataType) {
          filterDataSource = column.filterData.substring(column.filterData.indexOf(':') + 1, column.filterData.length)
          selectControl = header.find('.bootstrap-table-filter-control-'.concat(escapeID(column.field)))
          addOptionToSelectControl(selectControl, '', column.filterControlPlaceholder, column.filterDefault)
          filterDataType(filterDataSource, selectControl, that.options.filterOrderBy, column.filterDefault)
        } else {
          throw new SyntaxError('Error. You should use any of these allowed filter data methods: var, obj, json, url, func.' + ' Use like this: var: {key: "value"}')
        }
      }
    })

    if (addedFilterControl) {
      header.off('keyup', 'input').on('keyup', 'input', function (_ref4, obj) {
        const currentTarget = _ref4.currentTarget
        let keyCode = _ref4.keyCode
        syncControls(that) // Simulate enter key action from clear button

        keyCode = obj ? obj.keyCode : keyCode

        if (that.options.searchOnEnterKey && keyCode !== 13) {
          return
        }

        if ($__default.default.inArray(keyCode, [37, 38, 39, 40]) > -1) {
          return
        }

        const $currentTarget = $__default.default(currentTarget)

        if ($currentTarget.is(':checkbox') || $currentTarget.is(':radio')) {
          return
        }

        clearTimeout(currentTarget.timeoutId || 0)
        currentTarget.timeoutId = setTimeout(function () {
          that.onColumnSearch({
            currentTarget: currentTarget,
            keyCode: keyCode
          })
        }, that.options.searchTimeOut)
      })
      header.off('change', 'select:not(".ms-offscreen")').on('change', 'select:not(".ms-offscreen")', function (_ref5) {
        const currentTarget = _ref5.currentTarget
        const keyCode = _ref5.keyCode
        syncControls(that)
        const $select = $__default.default(currentTarget)
        const value = $select.val()

        if (value && value.length > 0 && value.trim()) {
          $select.find('option[selected]').removeAttr('selected')
          $select.find('option[value="'.concat(value, '"]')).attr('selected', true)
        } else {
          $select.find('option[selected]').removeAttr('selected')
        }

        clearTimeout(currentTarget.timeoutId || 0)
        currentTarget.timeoutId = setTimeout(function () {
          that.onColumnSearch({
            currentTarget: currentTarget,
            keyCode: keyCode
          })
        }, that.options.searchTimeOut)
      })
      header.off('mouseup', 'input:not([type=radio])').on('mouseup', 'input:not([type=radio])', function (_ref6) {
        const currentTarget = _ref6.currentTarget
        const keyCode = _ref6.keyCode
        const $input = $__default.default(currentTarget)
        const oldValue = $input.val()

        if (oldValue === '') {
          return
        }

        setTimeout(function () {
          syncControls(that)
          const newValue = $input.val()

          if (newValue === '') {
            clearTimeout(currentTarget.timeoutId || 0)
            currentTarget.timeoutId = setTimeout(function () {
              that.onColumnSearch({
                currentTarget: currentTarget,
                keyCode: keyCode
              })
            }, that.options.searchTimeOut)
          }
        }, 1)
      })
      header.off('change', 'input[type=radio]').on('change', 'input[type=radio]', function (_ref7) {
        const currentTarget = _ref7.currentTarget
        const keyCode = _ref7.keyCode
        clearTimeout(currentTarget.timeoutId || 0)
        currentTarget.timeoutId = setTimeout(function () {
          syncControls(that)
          that.onColumnSearch({
            currentTarget: currentTarget,
            keyCode: keyCode
          })
        }, that.options.searchTimeOut)
      })

      if (header.find('.date-filter-control').length > 0) {
        $__default.default.each(that.columns, function (i, _ref8) {
          const filterDefault = _ref8.filterDefault
          const filterControl = _ref8.filterControl
          const field = _ref8.field
          const filterDatepickerOptions = _ref8.filterDatepickerOptions

          if (filterControl !== undefined && filterControl.toLowerCase() === 'datepicker') {
            const $datepicker = header.find('.date-filter-control.bootstrap-table-filter-control-'.concat(field))
            $datepicker.datepicker(filterDatepickerOptions)

            if (filterDefault) {
              $datepicker.datepicker('setDate', filterDefault)
            }

            $datepicker.on('changeDate', function (_ref9) {
              const currentTarget = _ref9.currentTarget
              const keyCode = _ref9.keyCode
              clearTimeout(currentTarget.timeoutId || 0)
              currentTarget.timeoutId = setTimeout(function () {
                syncControls(that)
                that.onColumnSearch({
                  currentTarget: currentTarget,
                  keyCode: keyCode
                })
              }, that.options.searchTimeOut)
            })
          }
        })
      }

      if (that.options.sidePagination !== 'server' && !that.options.height) {
        that.triggerSearch()
      }

      if (!that.options.filterControlVisible) {
        header.find('.filter-control, .no-filter-control').hide()
      }
    } else {
      header.find('.filter-control, .no-filter-control').hide()
    }

    that.trigger('created-controls')
  }
  function getDirectionOfSelectOptions (_alignment) {
    const alignment = _alignment === undefined ? 'left' : _alignment.toLowerCase()

    switch (alignment) {
      case 'left':
        return 'ltr'

      case 'right':
        return 'rtl'

      case 'auto':
        return 'auto'

      default:
        return 'ltr'
    }
  }
  function syncControls (that) {
    if (that.options.height) {
      const controlsTableHeader = that.$tableHeader.find(searchControls)
      that.$header.find(searchControls).each(function (_, control) {
        const $control = $__default.default(control)
        const controlClass = getElementClass($control)
        const foundControl = controlsTableHeader.filter(function (_, ele) {
          const eleClass = getElementClass($__default.default(ele))
          return controlClass === eleClass
        })

        if (foundControl.length === 0) {
          return
        }

        if ($control.is('select')) {
          $control.find('option:selected').removeAttr('selected')
          $control.find("option[value='".concat(foundControl.val(), "']")).attr('selected', true)
        } else {
          $control.val(foundControl.val())
        }
      })
    }
  }
  var filterDataMethods = {
    func: function func (filterDataSource, selectControl, filterOrderBy, selected) {
      const variableValues = window[filterDataSource].apply() // eslint-disable-next-line guard-for-in

      for (const key in variableValues) {
        addOptionToSelectControl(selectControl, key, variableValues[key], selected)
      }

      sortSelectControl(selectControl, filterOrderBy)
    },
    obj: function obj (filterDataSource, selectControl, filterOrderBy, selected) {
      const objectKeys = filterDataSource.split('.')
      const variableName = objectKeys.shift()
      let variableValues = window[variableName]

      if (objectKeys.length > 0) {
        objectKeys.forEach(function (key) {
          variableValues = variableValues[key]
        })
      } // eslint-disable-next-line guard-for-in

      for (const key in variableValues) {
        addOptionToSelectControl(selectControl, key, variableValues[key], selected)
      }

      sortSelectControl(selectControl, filterOrderBy)
    },
    var: function _var (filterDataSource, selectControl, filterOrderBy, selected) {
      const variableValues = window[filterDataSource]
      const isArray = Array.isArray(variableValues)

      for (const key in variableValues) {
        if (isArray) {
          addOptionToSelectControl(selectControl, variableValues[key], variableValues[key], selected)
        } else {
          addOptionToSelectControl(selectControl, key, variableValues[key], selected)
        }
      }

      sortSelectControl(selectControl, filterOrderBy)
    },
    url: function url (filterDataSource, selectControl, filterOrderBy, selected) {
      $__default.default.ajax({
        url: filterDataSource,
        dataType: 'json',
        success: function success (data) {
          // eslint-disable-next-line guard-for-in
          for (const key in data) {
            addOptionToSelectControl(selectControl, key, data[key], selected)
          }

          sortSelectControl(selectControl, filterOrderBy)
        }
      })
    },
    json: function json (filterDataSource, selectControl, filterOrderBy, selected) {
      const variableValues = JSON.parse(filterDataSource) // eslint-disable-next-line guard-for-in

      for (const key in variableValues) {
        addOptionToSelectControl(selectControl, key, variableValues[key], selected)
      }

      sortSelectControl(selectControl, filterOrderBy)
    }
  }

  exports.addOptionToSelectControl = addOptionToSelectControl
  exports.collectBootstrapCookies = collectBootstrapCookies
  exports.copyValues = copyValues
  exports.createControls = createControls
  exports.escapeID = escapeID
  exports.existOptionInSelectControl = existOptionInSelectControl
  exports.fixHeaderCSS = fixHeaderCSS
  exports.getControlContainer = getControlContainer
  exports.getCursorPosition = getCursorPosition
  exports.getDirectionOfSelectOptions = getDirectionOfSelectOptions
  exports.getElementClass = getElementClass
  exports.getFilterDataMethod = getFilterDataMethod
  exports.getOptionsFromSelectControl = getOptionsFromSelectControl
  exports.getSearchControls = getSearchControls
  exports.hasSelectControlElement = hasSelectControlElement
  exports.hideUnusedSelectOptions = hideUnusedSelectOptions
  exports.initFilterSelectControls = initFilterSelectControls
  exports.isColumnSearchableViaSelect = isColumnSearchableViaSelect
  exports.isFilterDataNotGiven = isFilterDataNotGiven
  exports.setCursorPosition = setCursorPosition
  exports.setValues = setValues
  exports.sortSelectControl = sortSelectControl
  exports.syncControls = syncControls

  Object.defineProperty(exports, '__esModule', { value: true })
}))
