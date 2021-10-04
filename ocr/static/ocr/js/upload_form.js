/* eslint no-unused-vars:0 */
function submitForm(form) {
  const url = form.attr('action');
  const formData = {};
  $(form).find('input[id]').each((index, node) => {
    formData[node.id] = node.value;
  });
  $.post(url, formData).done((data) => {});
}
