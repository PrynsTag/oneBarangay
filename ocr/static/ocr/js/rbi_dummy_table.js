function createdFormatter(value) {
  return moment(value).format('dddd, MMMM Do YYYY, h:mm:ss:SSS A');
}

/* eslint no-unused-vars:0 */
function dateFormatter(value) {
/* eslint no-undef:0 */
  return moment(value, 'YYYY-MM-DD').format('dddd, MMMM Do YYYY');
}

$(document).ready(() => {
  $('.bootstrap-table')
    .addClass('bootstrap5')
    .removeClass('bootstrap4');
});
