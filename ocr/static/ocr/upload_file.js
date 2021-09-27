const submitBtn = document.getElementById('submit')
const removeLink = document.getElementsByClassName('dz-remove')
const scanBtn = document.getElementById('scan')

Dropzone.autoDiscover = false

const myDropzone = new Dropzone('#my-awesome-dropzone', {
  autoProcessQueue: false,
  paramName: 'files',
  uploadMultiple: true,
  parallelUploads: 10,
  maxFileSize: 130000000,
  addRemoveLinks: true,
  acceptedFiles: 'image/jpeg,image/png,image/jpg,image/tiff,application/pdf',
  init: function () {
    const myDropzone = this

    this.on('addedfile', file => {
      console.log('A file has been added.')
      submitBtn.removeAttribute('hidden')
    })

    submitBtn.addEventListener('click', function () {
      myDropzone.processQueue()
      submitBtn.hidden = true
    })

    this.on('sending', function (file, xhr, formData) {
      console.log('sending')
      formData.append('fileData', JSON.stringify({
        last_modified: file.lastModifiedDate,
        size: file.upload.total,
        name: file.name,
        uuid: file.upload.uuid
      }))
    })
    this.on('complete', function () {
      removeLink[0].remove()
      scanBtn.removeAttribute('hidden')
    })
  }
})
