// Created as a part of the Verifying Quotations from Johnson's Dictionary project.
// Author: Drew  Schilling

// Export function
function exportMatches() {
  let exportURL = "php/export.php";
  let exportForm = $("#exportForm");
  let exportCriteria = exportForm.serialize();
  exportCriteria += "&token=" + token;
  //console.log(exportCriteria);
  $("#mask").addClass("loading");

  $.ajax({
    type: "POST",
    contentType: "application/x-www-form-urlencoded; charset=UTF-8",
    url: exportURL,
    //dataType: "application/octet-stream",
    data: exportCriteria,
    success: function(json) {
      //console.log(json);
      var jsonData = JSON.parse(json);
      var zipData = "filepath="+ jsonData.filepath + "&token=" + token;
      var zipURL = "php/exportzip.php";
      window.open("php/exportzip.php?" + zipData);
      $("#mask").removeClass("loading");
    },
    error: function(responseText, data) {
      console.log(data);
      console.log(responseText);
      alert("Error: Export failed.");
    }
  })
}

// Creates the match subtable header row. Also controls the column width.
function createMatchHeaderRowCols() {
  return `
  <th style="width:9%" id="scoreHeader">Match Rating</th>
  <th style="width:21%" id="matchQuoteHeader">Sourced Quote</th>
  <th style="width:16%" id="matchTitleHeader">Title</th>
  <th style="width:16%" id="matchAuthorHeader">Author</th>
  <th style="width:10%" id="flagHeader">Mark best?</th>
  <th style="width:19%" id="urlHeader">URL to Source</th>
  `
  //<th style="width:14%" id="matchIDHeader">Match ID</th>
}

function createMatchRowCols(row, cols, quoteID) {
  let data = JSON.parse(JSON.stringify(row));
  var markedBest = "";
  if (data.best_match) {
    markedBest = "checked";
  }
  // Store quote ID in Best Match column. This value will be used to evaluate all matches for that quote
  // ID to make sure only one best match is selected at a time.
  return `
    <td id="ratingCol" scope="row">${data.score}</td>
    <td id="matchQuoteCol">${data.content}</td>
    <td id="matchTitleCol">${data.title}</td>
    <td id="matchAuthorCol">${data.author}</td>
    <td id="flagCol" data-matchID="${data.match_id}" data-work_metadataID="${data.work_metadata_id}"><input type="radio" id="bestFlag" name="${quoteID}" ${markedBest}></td>
    <td id="urlCol">${data.url}</td>
  `
  //<td id="matchIDCol">${data.matchID}</td>
}

// Updates the chosen search type in Search Options and enables/disables the search box/dropdown 
// depending on the selected search.
function updateSearchOption(searchOption) {
  $("#chosenSearchOption").attr("value", searchOption);
    switch(searchOption) {
      case ('get_matches_by_headword'):
        $("#chosenSearch").html("Matches by Headword");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchRandRow").prop("hidden", true);
          $("#searchText").prop("disabled", false);
          $("#textFormatDropdown").prop("disabled", false);
          $("#searchTextRow").prop("hidden", false);
        }
        break;
      case ("get_matches_by_author"):
        $("#chosenSearch").html("Matches by Author");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchRandRow").prop("hidden", true);
          $("#searchText").prop("disabled", false);
          $("#textFormatDropdown").prop("disabled", false);
          $("#searchTextRow").prop("hidden", false);
        }
        break;
      case ("get_matches_by_title"):
        $("#chosenSearch").html("Matches by Title");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchRandRow").prop("hidden", true);
          $("#searchText").prop("disabled", false);
          $("#textFormatDropdown").prop("disabled", false);
          $("#searchTextRow").prop("hidden", false);
        }
        break;
      case ("get_matches_by_random"):
        $("#chosenSearch").html("Random Selection");
        if($("#searchTextCol").is(":visible")) {
          $("#searchText").prop("disabled", true);
          $("#textFormatDropdown").prop("disabled", true)
          $("#searchTextRow").prop("hidden", true);
          $("#searchRandomDropdown").prop("disabled", false);
          $("#searchRandRow").prop("hidden", false);
        }
        break;
    }
}

function floatingBarLoadHandler() {
  var params;
  (window.onpopstate = function () {
      var match,
          pl     = /\+/g,  // Regex for replacing addition symbol with a space
          search = /([^&=]+)=?([^&]*)/g,
          decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
          query  = window.location.search.substring(1);

      params = {};
      while (match = search.exec(query))
         params[decode(match[1])] = decode(match[2]);
  })();

  // Prevent HTML injection
  var searchTerm = "" + params["searchBox"];

  switch (params["chosenSearchOption"]) {
    case ('get_matches_by_headword'):
      $("#searchTypeHeader").html("Matches by Headword: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html("\"" + searchTerm + "\"");
      break;
    case ("get_matches_by_author"):
      $("#searchTypeHeader").html("Matches by Author: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html("\"" + searchTerm + "\"");
      break;
    case ("get_matches_by_title"):
      $("#searchTypeHeader").html("Matches by Title: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html("\"" + searchTerm + "\"");
      break;
    case ("get_matches_by_random"):
      $("#searchTypeHeader").html("Random Selection: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html(params["number"] + " quotes");
      break;
  }

}

function loadedHandler() {

  // Set token
  if (!(window.location.href.includes("login.php")) && !(window.location.href.includes("logout.php")) && !(window.location.href.includes("login.html"))){
    $("#tokenInput").attr("value", token);
  }

  // Decodes the search paramaters from the url with a regex and stores in searchParameters array.
  // Access the array with searchParameters["<formNameValue>"].
  var searchParameters;
  (window.onpopstate = function () {
      var match,
          pl     = /\+/g,  // Regex for replacing addition symbol with a space
          search = /([^&=]+)=?([^&]*)/g,
          decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
          query  = window.location.search.substring(1);

      searchParameters = {};
      while (match = search.exec(query))
         searchParameters[decode(match[1])] = decode(match[2]);
  })();

  var serialData = window.location.search.substring(1);
  var table;
  var url = "php/" + searchParameters["chosenSearchOption"] + ".php";
  if (window.location.href.includes("results.php")){
    $("#dataTablesEx, #mask").addClass("loading");

    // Execute the search and retrieve the quote JSON.
    $.ajax({
      type: "POST",
      contentType: "application/x-www-form-urlencoded; charset=UTF-8",
      url: url,
      dataType: "json",
      data: serialData,
      success: function(json) {
        //console.log(json);
        $("#dataTablesEx, #mask").removeClass("loading");
        
        // DataTables (v1.10.24) search results grid.
        // https://datatables.net/manual/
        // This DataTable uses the Buttons (v1.7.0), FixedHeader (v3.1.8), and Scroller (v2.0.3) extensions.
        // https://datatables.net/extensions/index
        table = $("#dataTablesEx").DataTable({
        "data": json,
        "dataSrc": "",
        // Set default to order by headword
        "order": [[ 1, "asc"]],
          "columns": [
            {"data": "best_marked_by",
            "width": "5%",
            "render": function(td, data, cellData, rowData, row, col) {
              $(col).attr("id", "markedCol");
              if (cellData.best_marked_by == null)
              {
                $(td).attr("");
                return 'Default';
              }
              else {
                return 'User-set';
              }
            },
          "createdCell": function(td, cellData, rowData, row, col) {
            $(td).attr("id", "markedCol");
          }},
            {"data": "headword",
            "width": "10%",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "headwordCol");
                $(td).attr("scope", "row");
                $(td).closest("tr").attr("id", "quoteRow");
                $(td).closest("tr").attr("data-quoteID", rowData.quote_id);
            }},
            {"data": "content",
            "width": "35%",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "quoteCol");
            }},
            {"data": "title",
            "width": "20%",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "quoteTitleCol");
            }},
            {"data": "author",
            "width": "15%",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "quoteAuthorCol");
            }},
            {"data": "edition",
            "width": "10%",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "editionCol");
                if (cellData == "both") {
                  $(td).html("1/4");
                }
            }}
          ],
          "deferRender": true,
          "fixedHeader": true,
          "fixedFooter": true

        });
      },
      error: function(data){
        $("#mask").removeClass("loading");
        console.log("error retrieving quote data.");
        console.log(data);
      }

    });
  }

  // Match subtable handler
  $("#dataTablesEx").on("click", "tbody tr td", function() {
    var tr = $(this).closest("tr");
    var row = table.row(tr);
    var tMin = searchParameters["tMin"];
    var tMax = searchParameters["tMax"];
    var searchCorpus = searchParameters["searchCorpus"];

    if (tr.attr("id") == "quoteRow") {
      var serialData = "quote_id=" + row.data().quote_id + "&tMin=" + tMin + "&tMax=" + tMax + "&searchCorpus=" + searchCorpus;
      if (row.child.isShown()){
        row.child.hide();
        tr.removeClass("shown");
      }
      else {
        $.ajax({
          type: "POST",
          contentType: "application/x-www-form-urlencoded; charset=UTF-8",
          url: "php/get_quote_matches.php",
          dataType: "json",
          data: serialData,
          success: function(responseData) {
            //console.log(responseData);
            row.child(createMatchTable(responseData, row.data().quote_id)).show();
            tr.addClass("shown");
          },
          error: function(data) {
            console.log(data);
            alert("Something went wrong when retrieving match data.");
          }
        });
        tr.addClass("shown");
      }
    }
  });

  // Best Match handlers
  
  $("body").on("mousedown", "#flagCol input[type='radio']", function() {

    var wasChecked = $(this).prop("checked");
    this.turnOff = wasChecked;
    //$(this).prop('checked', !wasChecked);

  });

  $("body").on("click", "#flagCol input[type='radio']", function(){
    clickedInput = $(this);
    var matchID = clickedInput.closest("td").attr("data-matchID");
    var work_metadataID = clickedInput.closest("td").attr("data-work_metadataID");
    var quoteID = clickedInput.attr("name");
    var serialData = "token=" + token + "&quote_id=" + quoteID +  "&match_id=" + matchID + "&work_metadata_id=" + work_metadataID;
    //console.log(serialData);

    // This button was checked: add its match to the best_matches table
    if (!this.turnOff)
    {
      //alert("checking!");
      var url = "php/set_best_match.php";
      $.ajax({
        type: "POST",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: url,
        data: serialData,
        success: function(data) {
          //console.log(data);
          //alert("Best match added.");
          clickedInput.prop("checked", !this.turnOff);
          this["turning-off"] = !this.turnOff;
          // Set this match's quote row's "marked by" column
          clickedInput.closest("td").closest("tr").closest("table").closest("tr").prev("tr").find("#markedCol").html("User-set");
        },
        error: function(data) {
          console.log(data);
          alert("Error. Best match not added.");
        }
      });
    }
    // This button was unchecked: reset its quote's Best Match to the default
    else {
    //alert("unchecking");
      var url = "php/unset_best_match.php";
      $.ajax({
        type: "POST",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: url,
        data: serialData,
        success: function() {
          clickedInput.prop("checked", false);
          // Set this quote's  Best Match back to the match with the highest score (the first match in the subtable)
          //clickedInput.closest("td").closest("tr").closest("tbody").find("tr").find("#flagCol input[type='radio']").prop("checked", true);
          this["turning-off"] = !this.turnOff;
          // Set this match's quote row's "marked by" column
          clickedInput.closest("td").closest("tr").closest("table").closest("tr").prev("tr").find("#markedCol").html("Default");
        },
        error: function() {
          alert("Error. Best match not removed.");
        }
      });
    }
  });

}

// Create the match subtable on quote row click.
function createMatchTable(matchData, quoteID) {
  let headerRow = createMatchHeaderRowCols();
  // Check if the quote has any matches. If not, use an empty matches table.
  if (matchData.length == 0) {
    headerRow = `<th style="width:100%" id="emptyHeader" colspan="5">No Matches</th>`
    return `
      <table id="matchTable" class="table table-bordered">
        <thead>
          <tr>
            ${headerRow}
          </tr>
        </thead>
          <td id="noMatchesFoundDatum" colspan="5">No matches found. Either this quote has no matches, or matches may have been filtered by search options.</td>
      </table>
      `
  }
  let cols = Object.keys(matchData[0]);

  let rows = matchData
    .map(row => {
      //let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
      let tds = createMatchRowCols(row, cols, quoteID);
      return `<tr>
                ${tds}
              </tr>`;
    })
    .join("");

  // Note: no tbody tags needed; Boostrap generates tbody tags around tr tags.
  return `
    <table id="matchTable" class="table table-bordered">
      <thead>
        <tr>
          ${headerRow}
        </tr>
      </thead>
        ${rows}
    </table>
  `
}

$(document).ready(loadedHandler);
$("#floatingBar").ready(floatingBarLoadHandler);
