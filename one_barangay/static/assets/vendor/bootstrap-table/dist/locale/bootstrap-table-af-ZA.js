(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('jquery'))
    : typeof define === 'function' && define.amd ? define(['jquery'], factory)
      : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.jQuery))
}(this, function ($) {
  'use strict'

  function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { default: e } }

  const $__default = /* #__PURE__ */_interopDefaultLegacy($)

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

  const document = global_1.document
  // typeof document.createElement is 'object' in old IE
  const EXISTS = isObject(document) && isObject(document.createElement)

  const documentCreateElement = function (it) {
	  return EXISTS ? document.createElement(it) : {}
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

  const aFunction = function (variable) {
	  return typeof variable === 'function' ? variable : undefined
  }

  const getBuiltIn = function (namespace, method) {
	  return arguments.length < 2 ? aFunction(path[namespace]) || aFunction(global_1[namespace])
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
  const createMethod = function (IS_INCLUDES) {
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
	  includes: createMethod(true),
	  // `Array.prototype.indexOf` method
	  // https://tc39.es/ecma262/#sec-array.prototype.indexof
	  indexOf: createMethod(false)
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
	 * Bootstrap Table Afrikaans translation
	 * Author: Phillip Kruger <phillip.kruger@gmail.com>
	 */

  $__default.default.fn.bootstrapTable.locales['af-ZA'] = $__default.default.fn.bootstrapTable.locales.af = {
	  formatCopyRows: function formatCopyRows () {
	    return 'Copy Rows'
	  },
	  formatPrint: function formatPrint () {
	    return 'Print'
	  },
	  formatLoadingMessage: function formatLoadingMessage () {
	    return 'Besig om te laai, wag asseblief'
	  },
	  formatRecordsPerPage: function formatRecordsPerPage (pageNumber) {
	    return ''.concat(pageNumber, ' rekords per bladsy')
	  },
	  formatShowingRows: function formatShowingRows (pageFrom, pageTo, totalRows, totalNotFiltered) {
	    if (totalNotFiltered !== undefined && totalNotFiltered > 0 && totalNotFiltered > totalRows) {
	      return 'Resultate '.concat(pageFrom, ' tot ').concat(pageTo, ' van ').concat(totalRows, ' rye (filtered from ').concat(totalNotFiltered, ' total rows)')
	    }

	    return 'Resultate '.concat(pageFrom, ' tot ').concat(pageTo, ' van ').concat(totalRows, ' rye')
	  },
	  formatSRPaginationPreText: function formatSRPaginationPreText () {
	    return 'previous page'
	  },
	  formatSRPaginationPageText: function formatSRPaginationPageText (page) {
	    return 'to page '.concat(page)
	  },
	  formatSRPaginationNextText: function formatSRPaginationNextText () {
	    return 'next page'
	  },
	  formatDetailPagination: function formatDetailPagination (totalRows) {
	    return 'Showing '.concat(totalRows, ' rows')
	  },
	  formatClearSearch: function formatClearSearch () {
	    return 'Clear Search'
	  },
	  formatSearch: function formatSearch () {
	    return 'Soek'
	  },
	  formatNoMatches: function formatNoMatches () {
	    return 'Geen rekords gevind nie'
	  },
	  formatPaginationSwitch: function formatPaginationSwitch () {
	    return 'Wys/verberg bladsy nummering'
	  },
	  formatPaginationSwitchDown: function formatPaginationSwitchDown () {
	    return 'Show pagination'
	  },
	  formatPaginationSwitchUp: function formatPaginationSwitchUp () {
	    return 'Hide pagination'
	  },
	  formatRefresh: function formatRefresh () {
	    return 'Herlaai'
	  },
	  formatToggle: function formatToggle () {
	    return 'Wissel'
	  },
	  formatToggleOn: function formatToggleOn () {
	    return 'Show card view'
	  },
	  formatToggleOff: function formatToggleOff () {
	    return 'Hide card view'
	  },
	  formatColumns: function formatColumns () {
	    return 'Kolomme'
	  },
	  formatColumnsToggleAll: function formatColumnsToggleAll () {
	    return 'Toggle all'
	  },
	  formatFullscreen: function formatFullscreen () {
	    return 'Fullscreen'
	  },
	  formatAllRows: function formatAllRows () {
	    return 'All'
	  },
	  formatAutoRefresh: function formatAutoRefresh () {
	    return 'Auto Refresh'
	  },
	  formatExport: function formatExport () {
	    return 'Export data'
	  },
	  formatJumpTo: function formatJumpTo () {
	    return 'GO'
	  },
	  formatAdvancedSearch: function formatAdvancedSearch () {
	    return 'Advanced search'
	  },
	  formatAdvancedCloseButton: function formatAdvancedCloseButton () {
	    return 'Close'
	  },
	  formatFilterControlSwitch: function formatFilterControlSwitch () {
	    return 'Hide/Show controls'
	  },
	  formatFilterControlSwitchHide: function formatFilterControlSwitchHide () {
	    return 'Hide controls'
	  },
	  formatFilterControlSwitchShow: function formatFilterControlSwitchShow () {
	    return 'Show controls'
	  }
  }
  $__default.default.extend($__default.default.fn.bootstrapTable.defaults, $__default.default.fn.bootstrapTable.locales['af-ZA'])
}))
