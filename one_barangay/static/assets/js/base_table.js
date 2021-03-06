const $table = $('#table');
let selections = [];

function getIdSelections() {
  return $.map($table.bootstrapTable('getSelections'), (row) => row.uid);
}

$table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table load-success.bs.table custom-view-post-body.bs.table', () => {
    $('#remove').prop('disabled', !$table.bootstrapTable('getSelections').length);
    $('#edit').prop('disabled', !$table.bootstrapTable('getSelections').length);
    $('#add').prop('disabled', $table.bootstrapTable('getSelections').length);

    selections = getIdSelections();
});
$table.on('all.bs.table', (e, name, args) => {
    /* eslint no-console:0 */
    // console.log(name, args);
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
        if (!key.startsWith("_")) {
            html.push(`<p><b>${key.replace("_", " ").toUpperCase()}:</b> ${value}</p>`);
        }
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

function totalTextFormatter(data) {
    return 'Total';
}

function totalNameFormatter(data) {
    return data.length;
}

function createdFormatter(value) {
    return moment(value).format('dddd, MMMM Do YYYY, h:mm A');
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
