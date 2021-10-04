const submitBtn = document.getElementById('submit')
const removeLink = document.getElementsByClassName('dz-remove')
const scanBtn = document.getElementById('scan')

Dropzone.autoDiscover = false

/* eslint no-undef:0 */
const myDropzone = new Dropzone('#my-awesome-dropzone', {
  autoProcessQueue: false,
  paramName: 'files',
  uploadMultiple: true,
  parallelUploads: 10,
  maxFileSize: 130000000,
  addRemoveLinks: true,
  acceptedFiles: 'image/jpeg,image/png,image/jpg,image/tiff,application/pdf',
  init () {
    this.on('addedfile', () => {
      submitBtn.removeAttribute('hidden')
    })

    submitBtn.addEventListener('click', () => {
      myDropzone.processQueue()
      submitBtn.hidden = true
    })

    this.on('sending', (file, xhr, formData) => {
      formData.append('fileData', JSON.stringify({
        last_modified: file.lastModifiedDate,
        size: file.upload.total,
        name: file.name,
        uuid: file.upload.uuid
      }))
    })
    this.on('complete', () => {
      removeLink[0].remove()
      scanBtn.removeAttribute('hidden')
    })
  }
})
