const userModal = new bootstrap.Modal(document.getElementById('user-modal'));
const modalForm = document.getElementById('modal-form');
const $modalTitle = $('h5.modal-title');
const $modalSubmitBtn = $('#modal-submit-button');

const $uid = $('input[name=uid]');
const $name = $('input[name=display_name]');
const $email = $('input[name=email]');
const $role = $('select[name=role]');
const $disabled = $('select[name=disabled]');
const $phoneNumber = $('input[name=phone_number]');

$('#cancel-modal').on('click', () => {
  userModal.hide();
});
$('#close-modal').on('click', () => {
  userModal.hide();
});

// TODO: Add edit button in custom view.
function populateEditModal(data) {
  const editUrl = userManagementEdit.replace(/0/, data.uid?.toString());

  $('#modal-form').attr('action', editUrl);
  $modalTitle.html('Update User');
  $modalSubmitBtn.html('Update User');

  $uid.val(data.uid);
  $email.val(data.email);
  $role.val(data.role).change();
  $disabled.val(data.disabled === true ? 'True' : 'False').change();

  if (!data.phone_number.startsWith('None')) {
    $phoneNumber.val(data.phone_number);
  }
  if (!data.display_name.startsWith('None')) {
    $name.val(data.display_name);
  }

  userModal.show();
}

function editAccount(...data) {
  const userData = {};
  const keys = ['uid', 'display_name', 'email', 'role', 'phone_number', 'disabled'];
  data.forEach((element, index) => {
    userData[keys[index]] = element;
  });
  populateEditModal(userData);
}

function customViewFormatter(data) {
  const template = $('#profileTemplate').html();
  let view = '';
  $.each(data, (i, row) => {
    const image = row.photo_url === '' ? userManageDefaultImg : row.photo_url;
    const accountStatus = row.disabled === 'False' ? 'Enabled' : 'Disabled';
    const lastSignIn = row.last_sign_in === 'Unknown' ? 'Unknown' : `${row.last_sign_in} ago`;
    $.each(row, (key, _) => {
      if (row[key]) {
        /* eslint no-param-reassign:0 */
        row[key] = row[key] === '' ? null : row[key];
      }
    });
    view += template
      .replaceAll('%NAME%', row.display_name)
      .replace('%IMAGE%', image)
      .replaceAll('%ID%', row.uid)
      .replace('%COMPLAINT_LINK%', row.creation_date)
      .replaceAll('%EMAIL%', row.email)
      .replace('%AGE%', row.age)
      .replace('%FAMILY_ROLE%', row.remarks)
      .replaceAll('%USER_ROLE%', row.role)
      .replace('%ACTIVE%', lastSignIn)
      .replace('%CIVIL_STATUS%', row.civil_status)
      .replaceAll('%STATUS%', accountStatus)
      .replaceAll('%PHONE_NUMBER%', row.phone_number)
      .replace('%ADDRESS%', row.address);
  });
  return `<div class="row mx-0">${view}</div>`;
}

function emailVerifiedFormatter(value) {
  return (value === true ? 'Yes' : 'No');
}

/* eslint no-unused-vars:0 */
function accountStatusFormatter(value) {
  return (value === true ? 'Disabled' : 'Enabled');
}

/* eslint no-unused-vars:0 */
function lastSignInFormatter(value) {
  return `${value} ago`;
}

/* eslint no-unused-vars:0 */
function actionButton(id, action) {
/* eslint no-undef:0 */
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
      let url;
      let msg;
      if (action === 'delete') {
        url = userManagementDelete.replace(/0/, id?.toString());
        msg = `User ${id} is deleted successfully!`;
      } else if (action === 'reset') {
        url = userManagementReset.replace(/0/, id?.toString());
        msg = `Password reset sent to user ${id}!`;
      }
      sendToServer(url, msg);
    } else if (
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire('Cancelled', `User ${id} is safe :)`, 'info');
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
        const users = $table.bootstrapTable('getSelections');
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
            $.each(users, (_, user) => {
              const msg = users.length > 1
                ? `${users.length} users has been successfully deleted.`
                : `${users[0].email} has been deleted.`;
              $table.bootstrapTable('remove', { field: 'uid', values: user.uid });
              const deleteUrl = userManagementDelete.replace(/0/, user.uid?.toString());

              $.ajax({
                url: deleteUrl,
                headers: {
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': getCookie('csrftoken'),
                },
                success: () => {
                  $('#add').removeAttr('disabled');
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
            const msg = users.length > 1 ? `${users.length} users is safe :)` : `${users[0].email} is safe :)`;
            swalWithBootstrapButtons.fire('Cancelled', msg, 'info');
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
        const rows = $table.bootstrapTable('getSelections')[0];
        populateEditModal(rows);
      },
      attributes: {
        title: 'Edit a row in the table',
        id: 'edit',
      },
    },
    btnAdd: {
      name: 'add',
      text: 'Add a row',
      icon: 'fas fa-plus',
      event() {
        modalForm.reset();

        $('#modal-form').attr('action', userManagementHome);

        $modalTitle.html('Add User');
        $modalSubmitBtn.html('Add User');

        userModal.show();
      },
      attributes: {
        title: 'Add a row in the table',
        id: 'add',
      },
    },
  };
}

$(() => {
  customButtons();
});
