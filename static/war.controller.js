var warApp = angular.module('warApp', ['angular-jquery-autocomplete']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{? ').endSymbol('?}');
}).config(['$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

warApp.controller('WarCtrl', function ($scope, $http) {

    $scope.newWarSide = null;
    $scope.war = {};

    $scope.init = function(warId){
        $scope.warId = warId;
        $scope.csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();
        $http.get('/wars/'+warId+'/info').success(function(data) {
            $scope.war = data;
        });
    };

    $scope.AddWarSide = function(){

        $http.post(
            '/wars/'+$scope.warId+'/add_war_side',
            {name: $scope.newWarSide}
        ).success(function(data) {
            $scope.war = data;
        });

    };


});