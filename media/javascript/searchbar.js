var searchbarDebounceInputTiming = 300
var searchBarMinCharacters = 3
var searchbarValue = ''

var searchbarPendingRequest = null
var fetchSearchbarResultsFromApi = function () {
  if (searchbarPendingRequest) searchbarPendingRequest.abort('Canceled from user')

  if (searchbarValue.length < searchBarMinCharacters) {
    return hideSearchbarResults()
  }

  searchbarPendingRequest = $.ajax({
    url: '/api/quicksearch/',
    type: 'GET',
    data: {
      q: searchbarValue
    }
  })
    .done(function (response) {
      showSearchbarResults(response)
    })
    .fail(function (error) {
      if (error.statusText !== 'Canceled from user') {
        hideSearchbarResults()
      }
    })
}

var createSearchbarMoreItemList = function () {
  var link = '/search/?q=' + searchbarValue + '&type=file'
  var title = 'Ricerca libera per "' + searchbarValue + '"'

  return (
    '<li class="autocomplete-list-freesearch">' +
      '<a class="ml-1" href="' + link + '">' +
        '<svg class="icon icon-xs icon-primary search-icon">' +
          '<use xlink:href="/media/static/vendor/bootstrap-italia/svg/sprite.svg#it-search"></use>' +
        '</svg>' +
        '<span class="autocomplete-list-text">' +
          '<span>' + title + '</span>' +
        '</span>' +
        '<svg class="icon icon-xs icon-primary right-arrow-icon">' +
          '<use xlink:href="/media/static/vendor/bootstrap-italia/svg/sprite.svg#it-arrow-right"></use>' +
        '</svg>' +
      '</a>' +
    '</li>'
  )
}

var createSearchbarItemList = function (item) {
  if (!item) return ''

  var title = item.text
  var link = item.link
  var icon = 'it-file'
  var type = (item.model || '').toUpperCase()

  if (item.model === 'documento') icon = 'it-file'
  else if (item.model === 'progetto') icon = 'it-folder'
  else if (item.model === 'amministrazione') icon = 'it-pa'

  return (
    '<li>' +
      '<a href="' + link + '">' +
        '<svg class="icon icon-sm">' +
          '<use xlink:href="/media/static/vendor/bootstrap-italia/svg/sprite.svg#' + icon + '"></use>' +
        '</svg>' +
        '<span class="autocomplete-list-text">' +
          title + ' <em>' + type + '</em>' +
        '</span>' +
      '</a>' +
    '</li>'
  )
}

var showSearchbarResults = function (results) {
  var elementsList = results.map(createSearchbarItemList)
  elementsList.push(createSearchbarMoreItemList())
  $('#id_site_search_results').html(elementsList)
  $('#id_site_search_results').show()
}

var hideSearchbarResults = function () {
  $('#id_site_search_results').hide()
}

var SearchbarBlurEventListener = function (e) {
  if (!$(e.target).parents('.search-main .autocomplete-wrapper-big').length) {
    hideSearchbarResults()
    window.removeEventListener('click', SearchbarBlurEventListener)
  }
}

$(document).ready(function () {
  var form = $('#id_site_form')
  var input = $('#id_site_search')

  // If input start with value, assign it to variable search
  searchbarValue = input ? input.val() : ''

  // Prevent form submit with ENTER key
  form.on('submit', function (e) {
    e.preventDefault()

    if (searchbarValue.length) {
      window.location.href = '/search/?q=' + searchbarValue + '&type=file'
    }
  })

  input.on('paste keyup', _debounce(function () {
    searchbarValue = $(this).val()
    fetchSearchbarResultsFromApi()
  }, searchbarDebounceInputTiming))

  input.on('focus', function () {
    searchbarValue = $(this).val()

    if (searchbarValue.length) {
      fetchSearchbarResultsFromApi()
    } else {
      // TODO: Chiamare qui le ricerce frequenti
    }

    window.addEventListener('click', SearchbarBlurEventListener)
  })
})

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
var _debounce = function (func, wait, immediate) {
  var timeout

  return function () {
    var context = this
    var args = arguments

    var later = function () {
      timeout = null
      if (!immediate) func.apply(context, args)
    }

    var callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)

    if (callNow) {
      func.apply(context, args)
    }
  }
}
