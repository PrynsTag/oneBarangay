(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('vue'))
    : typeof define === 'function' && define.amd ? define(['vue'], factory)
      : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.BootstrapTable = factory(global.vue))
}(this, function (vue) {
  'use strict'

  function _defineProperty (obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      })
    } else {
      obj[key] = value
    }

    return obj
  }

  function ownKeys$1 (object, enumerableOnly) {
    const keys = Object.keys(object)

    if (Object.getOwnPropertySymbols) {
      let symbols = Object.getOwnPropertySymbols(object)
      if (enumerableOnly) {
        symbols = symbols.filter(function (sym) {
          return Object.getOwnPropertyDescriptor(object, sym).enumerable
        })
      }
      keys.push.apply(keys, symbols)
    }

    return keys
  }

  function _objectSpread2 (target) {
    for (let i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {}

      if (i % 2) {
        ownKeys$1(Object(source), true).forEach(function (key) {
          _defineProperty(target, key, source[key])
        })
      } else if (Object.getOwnPropertyDescriptors) {
        Object.defineProperties(target, Object.getOwnPropertyDescriptors(source))
      } else {
        ownKeys$1(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key))
        })
      }
    }

    return target
  }

  function _toConsumableArray (arr) {
    return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread()
  }

  function _arrayWithoutHoles (arr) {
    if (Array.isArray(arr)) return _arrayLikeToArray(arr)
  }

  function _iterableToArray (iter) {
    if (typeof Symbol !== 'undefined' && Symbol.iterator in Object(iter)) return Array.from(iter)
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

  function _nonIterableSpread () {
    throw new TypeError('Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.')
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
  const floor$1 = Math.floor

  // `ToInteger` abstract operation
  // https://tc39.es/ecma262/#sec-tointeger
  const toInteger = function (argument) {
    return isNaN(argument = +argument) ? 0 : (argument > 0 ? floor$1 : ceil)(argument)
  }

  const min$2 = Math.min

  // `ToLength` abstract operation
  // https://tc39.es/ecma262/#sec-tolength
  const toLength = function (argument) {
    return argument > 0 ? min$2(toInteger(argument), 0x1FFFFFFFFFFFFF) : 0 // 2 ** 53 - 1 == 9007199254740991
  }

  const max$1 = Math.max
  const min$1 = Math.min

  // Helper for a popular repeating case of the spec:
  // Let integer be ? ToInteger(index).
  // If integer < 0, let result be max((length + integer), 0); else let result be min(integer, length).
  const toAbsoluteIndex = function (index, length) {
    const integer = toInteger(index)
    return integer < 0 ? max$1(integer + length, 0) : min$1(integer, length)
  }

  // `Array.prototype.{ indexOf, includes }` methods implementation
  const createMethod$1 = function (IS_INCLUDES) {
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
    includes: createMethod$1(true),
    // `Array.prototype.indexOf` method
    // https://tc39.es/ecma262/#sec-array.prototype.indexof
    indexOf: createMethod$1(false)
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

  // TODO: Remove from `core-js@4` since it's moved to entry points

  const SPECIES$2 = wellKnownSymbol('species')

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
        re.constructor[SPECIES$2] = function () { return re }
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

  // `ToObject` abstract operation
  // https://tc39.es/ecma262/#sec-toobject
  const toObject = function (argument) {
    return Object(requireObjectCoercible(argument))
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

  // `IsArray` abstract operation
  // https://tc39.es/ecma262/#sec-isarray
  const isArray = Array.isArray || function isArray (arg) {
    return classofRaw(arg) == 'Array'
  }

  const createProperty = function (object, key, value) {
    const propertyKey = toPrimitive(key)
    if (propertyKey in object) objectDefineProperty.f(object, propertyKey, createPropertyDescriptor(0, value))
    else object[propertyKey] = value
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

  const $ = window.jQuery

  const deepCopy = function deepCopy (arg) {
    if (arg === undefined) {
      return arg
    }

    return $.extend(true, Array.isArray(arg) ? [] : {}, arg)
  }

  const script = {
    name: 'BootstrapTable',
    props: {
      columns: {
        type: Array,
        require: true
      },
      data: {
        type: [Array, Object],
        default: function _default () {
          return undefined
        }
      },
      options: {
        type: Object,
        default: function _default () {
          return {}
        }
      }
    },
    mounted: function mounted () {
      const _this = this

      this.$table = $(this.$el)
      this.$table.on('all.bs.table', function (e, name, args) {
        let eventName = $.fn.bootstrapTable.events[name]
        eventName = eventName.replace(/([A-Z])/g, '-$1').toLowerCase()

        _this.$emit.apply(_this, ['on-all'].concat(_toConsumableArray(args)))

        _this.$emit.apply(_this, [eventName].concat(_toConsumableArray(args)))
      })

      this._initTable()
    },
    methods: _objectSpread2({
      _initTable: function _initTable () {
        const options = _objectSpread2(_objectSpread2({}, deepCopy(this.options)), {}, {
          columns: deepCopy(this.columns),
          data: deepCopy(this.data)
        })

        if (!this._hasInit) {
          this.$table.bootstrapTable(options)
          this._hasInit = true
        } else {
          this.refreshOptions(options)
        }
      }
    }, (function () {
      const res = {}

      const _iterator = _createForOfIteratorHelper($.fn.bootstrapTable.methods)
      let _step

      try {
        const _loop = function _loop () {
          const method = _step.value

          res[method] = function () {
            let _this$$table

            for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
              args[_key] = arguments[_key]
            }

            return (_this$$table = this.$table).bootstrapTable.apply(_this$$table, [method].concat(args))
          }
        }

        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          _loop()
        }
      } catch (err) {
        _iterator.e(err)
      } finally {
        _iterator.f()
      }

      return res
    }())),
    watch: {
      options: {
        handler: function handler () {
          this._initTable()
        },
        deep: true
      },
      columns: {
        handler: function handler () {
          this._initTable()
        },
        deep: true
      },
      data: {
        handler: function handler () {
          this.load(deepCopy(this.data))
        },
        deep: true
      }
    }
  }

  function render (_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createBlock('table')
  }

  script.render = render
  script.__file = 'src/vue/BootstrapTable.vue'

  return script
}))
