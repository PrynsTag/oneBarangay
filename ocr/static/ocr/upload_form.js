function submitForm (form) {
  const url = form.attr('action')
  const formData = {}
  $(form).find('input[id]').each(function (index, node) {
    formData[node.id] = node.value
  })
  $.post(url, formData).done(function (data) {
    alert(data)
  })
}
