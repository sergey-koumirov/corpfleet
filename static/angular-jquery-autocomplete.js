'use strict';
angular.module('angular-jquery-autocomplete', []).directive('autocomplete', function () {
    return {
        restrict: 'EA',
        scope: {
            resultId: '=',
            url: '@'
        },

        link: function (scope, elem, attr, ctrl) {

            var config = {
                source: function( request, response ) {
                    $.ajax({
                      url: scope.url,
                      data: {
                        term: request.term
                      },
                      success: function( data ) {
                        response( data );
                      }
                    });
                },
                minLength: 1,
                select: function (event, ui) {
                    this.value = ui.item.name;
                    scope.resultId = ui.item.id;

                    console.debug(scope.resultId);

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