var warApp = angular.module('warApp', ['angular-jquery-autocomplete']);

warApp.controller('WarCtrl', function ($scope, $http) {

    $scope.init = function(warId){
        $scope.warId = warId;
        $http.get('/wars/'+warId+'/info.json').success(function(data) {
//            $scope.calculator = data;
        });
    };


});