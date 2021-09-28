// import Dashboard from '/node_modules/@uppy/dashboard'
// import XHRUpload from '/node_modules/@uppy/xhr-upload'
// import Form from '/node_modules/@uppy/form'
// import Uppy from "/node_modules/@uppy/core"
var uppy = new Uppy.Core({
    id: 'uppy',
    autoProceed: false,
    allowMultipleUploadBatches: true,
    debug: false,
    restrictions: {
        maxFileSize: null,
        minFileSize: null,
        maxTotalFileSize: null,
        maxNumberOfFiles: null,
        minNumberOfFiles: null,
        allowedFileTypes: null,
        requiredMetaFields: [],
    },
    meta: {},
    onBeforeFileAdded: (currentFile, files) => currentFile,
    onBeforeUpload: (files) => {
    },
    locale: {},
    infoTimeout: 5000,
}).use(Uppy.Dashboard, {
    inline: true,
    target: '#drag-drop-area',
    showProgressDetails: true,
})
.use(Uppy.XHRUpload, {
    endpoint: '{% url "upload" %}',
    formData: true,
    fieldName: "files"
})
.use(Uppy.Form, {
    target: '#file-upload',
    submitOnSuccess: false,
    getMetaFromForm: true,
    addResultToForm: true,
    multipleResults: true,
    triggerUploadOnSubmit: true
})

uppy.on('complete', (result) => {
    console.log('Upload complete! We’ve uploaded these files:', result.successful)
})
