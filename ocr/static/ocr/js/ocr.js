const ocrModal = new bootstrap.Modal(document.getElementById('ocr-modal'));
const aTagRegex = new RegExp(/\d+/);

$('#cancel-modal').on('click', () => {
  ocrModal.hide();
});
$('#close-modal').on('click', () => {
  ocrModal.hide();
});

function sendToServer(url, msg) {
  $.ajax({
    url,
    type: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    success: () => {
      showSuccess(msg);
    },
    error: (errorThrown) => {
      showError(errorThrown);
    },
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* eslint no-unused-vars:0 */
function customViewFormatter(data) {
  const template = $('#profileTemplate').html();
  let view = '';
  $.each(data, (i, row) => {
    $.each(row, (key, _) => {
      if (row[key]) {
        /* eslint no-param-reassign:0 */
        row[key] = row[key] === '' ? null : row[key];
      }
    });
    const houseId = row.house_num.match(aTagRegex)[0];
    const familyTreeUrl = `/ocr/detail/${houseId}`;
    view += template
      .replaceAll('%HOUSE_NUM%', houseId)
      .replace('%FAMILY_TREE%', familyTreeUrl)
      .replace('%ADDRESS%', row.address)
      .replace('%STREET%', row.street)
      .replace('%FAMILY_NAME%', `${row.family_name}'s Family`);
  });
  return `<div class="row mx-0">${view}</div>`;
}

function redirectToEdit(urlTemplateTag, arg) {
  window.location.href = urlTemplateTag.replace(/0/, arg?.toString());
}

function getHouseNumber(aTag) {
  return aTag.match(aTagRegex)[0];
}

function actionButton(houseNum, action) {
  swalWithBootstrapButtons.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, do it!',
    cancelButtonText: 'No, cancel!',
    reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
      let url; let
        msg;
      if (action === 'edit') {
        url = editUrl.replace(/0/, houseNum?.toString());
        msg = `RBI with house number of ${houseNum} has been successfully edited!`;
      } else {
        url = deleteUrl.replace(/0/, houseNum?.toString());
        msg = `RBI with house number of ${houseNum} has been deleted successfully!`;
      }
      sendToServer(url, msg);
    } else if (
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire('Cancelled!', `RBI ${houseNum} is safe :)`, 'info');
    }
  });
}

function customButtons() {
  return {
    btnDelete: {
      name: 'delete',
      text: 'Delete a number of rows',
      icon: 'fas fa-trash',
      event: () => {
        const rows = $table.bootstrapTable('getSelections');
        swalWithBootstrapButtons.fire({
          title: 'Are you sure?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Yes, delete it!',
          cancelButtonText: 'No, cancel!',
          reverseButtons: true,
        }).then((result) => {
          if (result.isConfirmed) {
            $.each(rows, (id, row) => {
              const houseNum = row.house_num.match(aTagRegex)[0];
              /* eslint no-use-before-define:0 */
              const deleteUrl = deleteUrl.replace(/0/, houseNum?.toString());
              const msg = `RBI with house number of ${houseNum} has been successfully edited!`;

              $table.bootstrapTable('remove', { field: 'house_num', values: houseNum });
              $.ajax({
                url: deleteUrl,
                type: 'POST',
                headers: {
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': getCookie('csrftoken'),
                },
                success: () => {
                  showSuccess(msg);
                },
                error: (errorThrown) => {
                  showError(errorThrown);
                },
              });
            });
          } else if (
            result.dismiss === Swal.DismissReason.cancel
          ) {
            const msg = rows.length > 1 ? `${rows.length} RBI is safe :)` : `RBI ${rows[0].house_num} is safe :)`;
            swalWithBootstrapButtons.fire('Cancelled!', msg, 'info');
          }
        });
      },
      attributes: {
        title: 'Delete a number of rows',
        id: 'remove',
      },
    },
    btnEdit: {
      name: 'edit',
      text: 'Edit a row',
      icon: 'fas fa-edit',
      event() {
        // TODO: Toggle multiple edit when multiple rows is present.
        /* eslint no-undef:0 */
        const row = $table.bootstrapTable('getSelections')[0];
        const houseNum = getHouseNumber(row.house_num);
        redirectToEdit(editUrl, houseNum);
      },
      attributes: {
        title: 'Edit a row in the table',
        id: 'edit',
      },
    },
  };
}

$(() => {
  customButtons();
});
