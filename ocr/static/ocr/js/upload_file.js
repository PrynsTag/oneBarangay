const submitBtn = document.getElementById('submit');

/* eslint no-undef:0 */
Dropzone.options.ocrFileUpload = {
  autoProcessQueue: false,
  paramName: 'file_upload',
  uploadMultiple: true,
  parallelUploads: 10,
  maxFileSize: 20000000,
  addRemoveLinks: true,
  dictRemoveFile: '<i class="fas fa-trash-alt fw-normal text-danger"></i>'
      + '<span class="text-danger">'
      + ' Remove'
      + '</span>',
  dictDefaultMessage: 'Click Here or Drop Files To Upload'
      + '<br>'
      + '<br>'
      + '<span class="text-gray-400">Supported File Types: JPG, PNG, PDF (20MB Max.)</span>',
  acceptedFiles: 'image/jpeg,image/png,image/jpg,application/pdf',

  init() {
    const csrftoken = getCookie('csrftoken');
    const myDropzone = this;

    submitBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      myDropzone.processQueue();
    });

    myDropzone.on('addedfile', (files) => {
      const defaultImgThumbnail = document.querySelector('#preview').dataset.url;
      if (!files.type.match(/image.*/) || files.type.match(/application\/pdf/)) {
        // This is not an image, so Dropzone doesn't create a thumbnail.
        // Set a default thumbnail:
        myDropzone.emit('thumbnail', files, defaultImgThumbnail);
      }
      submitBtn.removeAttribute('hidden');
    });

    myDropzone.on('sending', (file, xhr) => {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    });

    myDropzone.on('error', (files, message) => {
      $(files.previewElement).find('.dz-error-message').text(message);
      window.location.reload();
      myDropzone.removeFile(files);
    });

    myDropzone.on('success', () => {
      submitBtn.hidden = true;
      showSuccess('Files uploaded successfully!');
      setTimeout(() => {
        window.location.reload();
      }, 2500);
    });

    myDropzone.on('complete', () => {
      myDropzone.removeAllFiles();
    });
  },
};
