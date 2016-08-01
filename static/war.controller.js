var warApp = angular.module('warApp', ['angular-jquery-autocomplete']);

warApp.controller('WarCtrl', function ($scope, $http) {

    $scope.newWarSide = null;

    $scope.init = function(warId){
        $scope.warId = warId;
        $scope.csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();
        $http.get('/wars/'+warId+'/info').success(function(data) {
//            $scope.calculator = data;
        });
    };

    $scope.AddWarSide = function(){
        $.post(
            '/wars/'+$scope.warId+'/add_war_side',
            {name: $scope.newWarSide},
            function(data) {
                console.debug('success');
            }
        )

    };


});