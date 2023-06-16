$(document).ready(function() {
    // Initialize Isotope
    var $grid = $('.document-container').isotope({
        itemSelector: '.card',
        layoutMode: 'fitRows',
        getSortData: {
            subject: '[class]',
            uploaddate: '.document-uploaddate parseInt'
        }
    });

    // Filter items on button click
    $('.filter-button-group').on('click', 'button', function() {
        var filterValue = $(this).attr('data-filter');
        $grid.isotope({ filter: filterValue });
    });

    // Sort items on button click
    $('.sort-by-button-group').on('click', 'button', function() {
        var sortByValue = $(this).attr('data-sort-by');
        $grid.isotope({ sortBy: sortByValue });
    });

    // Use value of search field to filter
    var qsRegex;
    var $quicksearch = $('.quicksearch').keyup(debounce(function() {
        qsRegex = new RegExp($quicksearch.val(), 'gi');
        $grid.isotope({
            filter: function() {
                return qsRegex ? $(this).text().match(qsRegex) : true;
            }
        });
    }, 200));

    // Debounce so filtering doesn't happen every millisecond
    function debounce(fn, threshold) {
        var timeout;
        return function debounced() {
            if (timeout) {
                clearTimeout(timeout);
            }
            var args = arguments;
            var _this = this;

            function delayed() {
                fn.apply(_this, args);
            }
            timeout = setTimeout(delayed, threshold || 100);
        };
    }
});