var lopputiliApp = angular.module('lopputiliApp', ['restangular', 'ui.router']);


lopputiliApp.config(function($stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/dashboard");
  //
  // Now set up the states
  var k = "static/partials/";
  $stateProvider
  .state('dashboard', {
    url: "/dashboard",
    templateUrl: k+"dashboard.html",
  })
  .state('invoices', {
    url: "/invoices",
    templateUrl: k+"invoices.html"
  })
  .state('contacts', {
    url: "/contacts",
    controller: 'ContactsCtrl',
    templateUrl: k+"contacts.html"
  })
  .state('settings', {
    url: "/settings",
    controller: 'SettingsCtrl',
    templateUrl: k+"settings.html"
  })
  .state('receipts', {
    url: "/receipts",
    controller: 'ReceiptsCtrl',
    templateUrl: k+"receipts.html"
  });
});

lopputiliApp.config(function(RestangularProvider) {
  RestangularProvider.setBaseUrl('/api');
    // add a response intereceptor
    RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
      var extractedData;
      // .. to look for getList operations
      if (operation === "getList") {
        // .. and handle the data and meta data
        extractedData = data.data;
        //extractedData.meta = data.data.meta;
      } else {
        extractedData = data;
      }
      return extractedData;
    });
    RestangularProvider.setRestangularFields({
      id: "pk"
    });
  });

lopputiliApp.controller('ReceiptsCtrl', function ($scope, Restangular) {
  $scope.accounts_by_pk = [];
  Restangular.all('accounts').getList().then(function (accounts) {
    $scope.accounts = accounts;
    accounts.forEach(function(account){
      $scope.accounts_by_pk[account.pk] = account;
    });
  });
  Restangular.all('receipts').getList().then(function (receipts) {
    $scope.receipts = receipts;
    console.log(receipts);
  });
  $scope.editReceipt = function edit_receipt (receipt) {
    $scope.selected = receipt;
    receipt.all('commits').getList().then(function (commits) {
      $scope.commits = commits;
      console.log("Commits", commits);
    });
  };
});


lopputiliApp.controller('ContactsCtrl', function ($scope, Restangular) {
  Restangular.all('contacts').getList().then(function (contacts) {
    $scope.contacts = contacts;
  });

  $scope.addContact = function add_contact (form) {
    Restangular.all('contacts').post(form).then(function(contact){
      $scope.contacts.push(contact);
      $scope.form = {};
      alertify.success("Yhteystieto lisätty!");
    }, function(error){
      console.log(error);
      alertify.error("Yhteystietoa ei voitu lisätä! ("+error.data.error+")");
    });
  };
  $scope.removeContact = function remove_contact (contact) {
    contact.remove().then(function(){
      $scope.contacts = _.without($scope.contacts, contact);
      alertify.success("Yhteystieto poistettu!");
    }, function(){
      alertify.error("Yhteystietoa ei voitu poistaa!");
    });
  };
});

lopputiliApp.controller('SettingsCtrl', function ($scope, Restangular) {
   Restangular.all('accounts').getList().then(function (accounts) {
    $scope.accounts = accounts;
  });
});