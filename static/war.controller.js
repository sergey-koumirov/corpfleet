var warApp = angular.module('warApp', ['angular-jquery-autocomplete']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{? ').endSymbol('?}');
}).config(['$httpProvider', function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

warApp.controller('WarCtrl', function ($scope, $http, $filter) {

    $scope.newWarSide = null;
    $scope.newTerritory = null;
    $scope.war = {};
    $scope.todayStr = $filter('date')(new Date(), 'yyyy-MM-dd');
    $scope.endOfTime = '9999-12-31 23:59:59';

    $scope.init = function(warId){
        $scope.warId = warId;
        $http.get('/wars/'+warId+'/info').success(function(data) {
            $scope.war = data;
        });
    };

    $scope.AddParticipant = function(){
        $http.post(
            '/wars/'+$scope.warId+'/add_participant',
            {name: $scope.newWarSide}
        ).success(function(data) {
            $scope.war = data;
            $scope.newWarSide = null;
        });
    };
    $scope.DeleteParticipant = function(warId, participantId){
        $http.post(
            '/wars/'+warId+'/participant/'+participantId+'/delete'
        ).success(function(data) {
            $scope.war = data;
        });
    };

    $scope.AddAlliance = function(participant){
        $http.post(
            '/wars/'+$scope.warId+'/participant/'+participant.id+'/add_alliance',
            {
                id: participant.newAllianceId,
                date1: participant.newDate1 || $scope.todayStr,
                date2: participant.newDate2 || $scope.endOfTime
            }
        ).success(function(data) {
            $scope.war = data;
            participant.newAllianceId = null;
            participant.newDate1 = null;
            participant.newDate2 = null;
        });
    };
    $scope.DeleteAlliance = function(warId, participantId, participantAllianceId){
        $http.post(
            '/wars/'+warId+'/participant/'+participantId+'/alliance/'+participantAllianceId+'/delete'
        ).success(function(data) {
            $scope.war = data;
        });
    };
    $scope.UpdateAlliance = function(warId, participantId, participantAlliance){
        $http.post(
            '/wars/'+warId+'/participant/'+participantId+'/alliance/'+participantAlliance.id+'/update',
            {
                date1: participantAlliance.date1,
                date2: participantAlliance.date2
            }
        ).success(function(data) {
            $scope.war = data;
        });
    };

    $scope.AddTerritory = function(){
        $http.post(
            '/wars/'+$scope.warId+'/add_territory',
            {name: $scope.newTerritory}
        ).success(function(data) {
            $scope.war = data;
            $scope.newTerritory = null;
        });
    };
    $scope.DeleteTerritory = function(warId, territoryId){
        $http.post(
            '/wars/'+warId+'/territory/'+territoryId+'/delete'
        ).success(function(data) {
            $scope.war = data;
        });
    };

    $scope.AddRegion = function(territory){
        $http.post(
            '/wars/'+$scope.warId+'/territory/'+territory.id+'/add_region',
            {id: territory.newRegionId}
        ).success(function(data) {
            $scope.war = data;
            territory.newRegionId = null;
        });
    };
    $scope.DeleteRegion = function(warId, territoryId, territoryRegionId){
        $http.post(
            '/wars/'+warId+'/territory/'+territoryId+'/region/'+territoryRegionId+'/delete'
        ).success(function(data) {
            $scope.war = data;
        });
    };


});