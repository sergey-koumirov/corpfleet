var warApp = angular.module('warApp', ['angular-jquery-autocomplete']);

warApp.controller('WarCtrl', function ($scope, $http) {

    $scope.init = function(warId){
        $scope.warId = warId;
        $scope.csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();
        $http.get('/wars/'+warId+'/info.json').success(function(data) {
//            $scope.calculator = data;
        });
    };

    $scope.AddWarSide = function(){
        var name = $('#newWarSide').val();

        $.ajax({
            url: '/wars/'+$scope.warId+'/add_war_side',
            typr: 'post',
            data: {
                name: name
            },
            success: function(data) {
                console.debug('success');
            }
        })

    };


});