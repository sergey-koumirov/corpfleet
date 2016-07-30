'use strict';
angular.module('angular-jquery-autocomplete', []).directive('autocomplete', function () {
    return {
        restrict: 'EA',
        scope: {
            resultId: '=',
            oreOnly: '='
        },

        link: function (scope, elem, attr, ctrl) {

            var config = {
                source: function( request, response ) {
                    $.ajax({
                      url: "/wars/alliances",
                      data: {
                        term: request.term,
                        ore: scope.oreOnly
                      },
                      success: function( data ) {
                        response( data );
                      }
                    });
                },
                minLength: 3,
                select: function (event, ui) {
                    this.value = ui.item.name;
                    scope.resultId = ui.item.id;
                    scope.$apply();
                    return false;
                },
                _renderItem: function( ul, item ) {
                    return $( "<li>" ).append( item.name ).appendTo( ul );
                }
            }
            if (config._renderItem){
                elem.autocomplete(config).autocomplete( "instance" )._renderItem = config._renderItem;
            }else{
                elem.autocomplete(config);
            }

        }
    };
});