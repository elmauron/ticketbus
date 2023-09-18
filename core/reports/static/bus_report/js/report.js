var tblReport = null;
var input_search;
var current_date;
var btnClearSearch;
var select_member;
var columns = [];
var report = {
    initTable: function () {
        tblReport = $('#tblReport').DataTable({
            autoWidth: false,
            destroy: true,
        });
        tblReport.settings()[0].aoColumns.forEach(function (value, index, array) {
            columns.push(value.sWidthOrig);
        });
    },
    list: function () {
        var parameters = {
            'action': 'search_report',
            'term': input_search.val(),
            'member': select_member.val()
        };
        tblReport = $('#tblReport').DataTable({
            destroy: true,
            autoWidth: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ''
            },
            order: [[0, 'asc']],
            paging: false,
            ordering: true,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat'
                },
                {
                    extend: 'pdfHtml5',
                    text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-flat',
                    title: '',
                    orientation: 'landscape',
                    pageSize: 'LEGAL',
                    download: 'open',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 18,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 13,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 8
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 11,
                                color: 'white',
                                fillColor: '#2d4154',
                                alignment: 'center'
                            }
                        };
                        doc.content[1].table.widths = columns;
                        doc.content[1].margin = [0, 35, 0, 0];
                        doc.content[1].layout = {};
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: current_date}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });

                    }
                }
            ],
            columns: [
                {"data": "name"},
                {"data": "category.name"},
                {"data": "exemplar.name"},
                {"data": "exemplar.brand.name"},
                {"data": "plaque"},
                {"data": "member.names"},
                {"data": "year"},
                {"data": "car_seats"},
                {"data": "car_disk"},
                {"data": "ticket_price"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, -5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {

    current_date = new moment().format('YYYY-MM-DD');
    input_search = $('input[name="search"]');
    btnClearSearch = $('.btnClearSearch');
    select_member = $('select[name="member"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    input_search.on('keyup', function () {
        report.list();
    });

    report.initTable();

    btnClearSearch.on('click', function () {
        input_search.val('');
        report.list();
    });

    btnClearSearch.click();

    select_member.on('change', function () {
        report.list();
    });
});