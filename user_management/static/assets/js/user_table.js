const $table = $('#table');

const userModal = new bootstrap.Modal(document.getElementById('user-modal'));
const modalForm = document.getElementById('modal-form');
const $modalTitle = $('h5.modal-title');
const $modalSubmitBtn = $('#modal-submit-button');

const $uid = $('input[name=uid]');
const $name = $('input[name=display_name]');
const $password = $('input[name=password]');
const $email = $('input[name=email]');
const $role = $('select[name=role]');
const $disabled = $('select[name=disabled]');
const $phoneNumber = $('input[name=phone_number]');
const uidEl = document.getElementById('uid');

let selections = [];

function getIdSelections() {
  return $.map($table.bootstrapTable('getSelections'), (row) => row.uid);
}

$('#cancel-modal').on('click', () => {
  userModal.hide();
});
$('#close-modal').on('click', () => {
  userModal.hide();
});

/* eslint no-unused-vars:0 */
function responseHandler(res) {
  $.each(res.rows, (i, row) => {
    /* eslint no-param-reassign:0 */
    row.state = $.inArray(row.id, selections) !== -1;
  });
  return res;
}

function detailFormatter(index, row) {
  const html = [];
  $.each(row, (key, value) => {
    html.push(`<p><b>${key}:</b> ${value}</p>`);
  });
  return html.join('');
}

function totalTextFormatter() {
  return 'Total';
}

function totalFormatter(data) {
  return data.length;
}

function dateFormatter(value) {
  /* eslint no-undef:0 */
  return moment(value).format('dddd, MMMM Do YYYY, h:mm:ss:SSS A');
}

function lastSignInFormatter(value) {
  return moment(value).fromNow();
}

function emailVerifiedFormatter(value) {
  return (value === true ? 'Yes' : 'No');
}

function accountStatusFormatter(value) {
  return (value === true ? 'Disabled' : 'Enabled');
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function initTable() {
  $table.bootstrapTable('destroy').bootstrapTable({
    smartDisplay: true,
    sortReset: true,
    stickyHeader: true,
    stickyHeaderOffsetLeft: parseInt($('body').css('padding-left'), 10),
    stickyHeaderOffsetRight: parseInt($('body').css('padding-right'), 10),
    theadClasses: 'thead-dark',
    classes: 'table table-striped table-bordered table-hover',
    columns: [
      [{
        field: 'state',
        checkbox: true,
        rowspan: 1,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'creation_date',
        title: 'Date Created',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
        formatter: dateFormatter,
        footerFormatter: totalTextFormatter,
      }, {
        field: 'uid',
        title: 'User #',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
        footerFormatter: totalFormatter,
      }, {
        field: 'display_name',
        title: 'Name',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'email',
        title: 'Email',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'phone_number',
        title: 'Phone Number',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'role',
        title: 'User Role',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'provider',
        title: 'Account Provider',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'last_sign_in',
        title: 'Last Sign-in',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        formatter: lastSignInFormatter,
      }, {
        field: 'email_verified',
        title: 'Email Verified',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        formatter: emailVerifiedFormatter,
      }, {
        field: 'disabled',
        title: 'Account Status',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        formatter: accountStatusFormatter,
      }, {
        field: 'photo_url',
        title: 'Profile Picture',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      },
      ],
      [],
    ],
  });
  $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table load-success.bs.table', () => {
    $('#remove').prop('disabled', !$table.bootstrapTable('getSelections').length);
    $('#edit').prop('disabled', !$table.bootstrapTable('getSelections').length);
    $('#add').prop('disabled', $table.bootstrapTable('getSelections').length);

    selections = getIdSelections();
  });
  $table.on('all.bs.table', (e, name, args) => {
    /* eslint no-console:0 */
    console.log(name, args);
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
            $.each(users, (id, user) => {
              $table.bootstrapTable('remove', { field: 'uid', values: user.uid });
              $.ajax({
                url: '/barangay-admin/user_management/delete_user',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({ payload: { uid: user.uid } }),
                headers: {
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': getCookie('csrftoken'),
                },
              }).always((jqXHR, textStatus, errorThrown) => {
                $('#add').removeAttr('disabled');

                if (jqXHR.status === 200 || jqXHR.status === 304) {
                  const msg = users.length > 1
                    ? `${users.length} users has been successfully deleted.`
                    : `${users[0].email} has been deleted.`;

                  swalWithBootstrapButtons.fire(
                    'Success!',
                    msg,
                    'success',
                  );
                } else {
                  swalWithBootstrapButtons.fire(
                    'Error!',
                    `Something went wrong.<br>${errorThrown}`,
                    'error',
                  );
                }
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

        $('#modal-form').attr('action', '/barangay-admin/user_management/edit_user');
        $modalTitle.html('Update User');
        $modalSubmitBtn.html('Update User');

        uidEl.hidden = false;
        $password.prop('required', false);

        $uid.val(rows.uid);
        $name.val(rows.display_name);
        $email.val(rows.email);
        $role.val(rows.role).change();
        $disabled.val(rows.disabled === true ? 'True' : 'False').change();
        $phoneNumber.val(rows.phone_number);

        userModal.show();
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

        uidEl.hidden = true;
        $('#modal-form').attr('action', '/barangay-admin/user_management/');
        $password.prop('required', false);

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
  initTable();

  // Replace bootstrap4 with bootstrap5
  $(document).ready(() => {
    $('.bootstrap-table')
      .addClass('bootstrap5')
      .removeClass('bootstrap4');
  });
});
