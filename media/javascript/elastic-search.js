// Qs is defined on readthedocs/templates/docsitalia/overrides/search/elastic_search.html on bottom

$(document).ready(function () {
  $('#order-select').on('change', function () {
    var selectedOrder = $(this).children('option:selected').val()
    var params = Qs.parse(window.location.search.replace('?', ''))

    // NOTE: Update this value if you want to change select default value
    var defaultValue = 'relevance'

    if (selectedOrder && selectedOrder !== defaultValue) {
      params.sort = selectedOrder
    } else {
      delete params.sort
    }

    var stringifiedParams = Qs.stringify(params, { arrayFormat: 'repeat' })
    window.location.href = window.location.origin + window.location.pathname + '?' + stringifiedParams
  })
})
