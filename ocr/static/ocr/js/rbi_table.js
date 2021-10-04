const $table = $('#table');
const $remove = $('#remove');
let selections = [];

function getIdSelections() {
  return $.map($table.bootstrapTable('getSelections'), (row) => row.id);
}

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

function operateFormatter(value, row, index) {
  return [
    '<a class="remove" href="javascript:void(0)" title="Remove">',
    '<i class="fas fa-trash"></i>',
    '</a>',
  ].join('');
}

window.operateEvents = {
/* eslint func-names:0 */
  'click .remove': function (e, value, row, index) {
    $table.bootstrapTable('remove', {
      field: 'id',
      values: [row.id],
    });
  },
};

function totalTextFormatter(data) {
  return 'Total';
}

function totalNameFormatter(data) {
  return data.length;
}

function createdFormatter(value) {
/* eslint no-undef:0 */
  return moment(value).format('dddd, MMMM Do YYYY, h:mm:ss:SSS A');
}

function dateFormatter(value) {
  return moment(value, 'YYYY-MM-DD').format('dddd, MMMM Do YYYY');
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
        field: 'created_at',
        title: 'Date Created',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
        footerFormatter: totalNameFormatter,
        formatter: createdFormatter,

      }, {
        field: 'house_num',
        title: 'House #',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
      }, {
        field: 'date_accomplished',
        title: 'Date Filled',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
        formatter: dateFormatter,
      }, {
        field: 'address',
        title: 'House Address',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
      }, {
        field: 'first_name',
        title: 'First Name',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'middle_name',
        title: 'Middle Name',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'last_name',
        title: 'Last Name',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'ext',
        title: 'Ext',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'sex',
        title: 'Gender',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'birth_date',
        title: 'Birth Date',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'birth_place',
        title: 'Birth Place',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'civil_status',
        title: 'Civil Status',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'monthly_income',
        title: 'Monthly Income',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'citizenship',
        title: 'Citizenship',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'remarks',
        title: 'Relationship to Head',
        sortable: true,
        rowspan: 2,
        align: 'center',
        valign: 'middle',
      }, {
        field: 'operate',
        title: 'Item Operate',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        clickToSelect: false,
        events: window.operateEvents,
        formatter: operateFormatter,
      }],
      [],
    ],
  });
  $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table',
    () => {
      $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);

      // save your data, here just save the current page
      selections = getIdSelections();
    // push or splice the selections if you want to save all data selections
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
        const ids = getIdSelections();
        $table.bootstrapTable('remove', {
          field: 'id',
          values: ids,
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
        // TODO: Implement Edit Row
      },
      attributes: {
        title: 'Edit a row in the table',
        id: 'edit',
      },
    },
  };
}

$(() => {
  initTable();
  customButtons();
  // Replace bootstrap4 with bootstrap5
  $(document).ready(() => {
    $('.bootstrap-table')
      .addClass('bootstrap5')
      .removeClass('bootstrap4');
  });
});
