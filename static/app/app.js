var lopputiliApp = angular.module('lopputiliApp', ['restangular', 'ui.router', 'xeditable']);


lopputiliApp.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

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
    controller: 'InvoicesCtrl',
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
  });
  $scope.editReceipt = function edit_receipt (receipt) {
    $scope.selected = receipt;
    receipt.all('commits').getList().then(function (commits) {
      $scope.commits = commits;
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
  $scope.updateContact = function update_contact (contact) {
    contact.save().then(function () {
      alertify.success("Yhteystieto tallennettu!");
    }, function () {
      alertify.error("Yhteystiedon tallentaminen epäonnistui");
    });
    return true;
  };
});

lopputiliApp.controller('SettingsCtrl', function ($scope, Restangular) {
  Restangular.all('accounts').getList().then(function (accounts) {
    $scope.accounts = accounts;
  });


  Restangular.one('settings').get().then(function (settings) {
    $scope.settings = settings;
  });

  $scope.saveSettings = function save_settings () {
    Restangular.one('settings').customPUT($scope.settings).then(function(){
      alertify.success("Asetukset tallennettu!"); },
      function(){
      alertify.error("Asetuksien tallentaminen epäonnistui");
    });
  };

  $scope.addAccount = function add_account (form) {
    form.aid = parseInt(form.aid);
    Restangular.all('accounts').post(form).then(function(account){
      $scope.accounts.push(account);
      $scope.form = {};
      alertify.success("Tili lisätty!");
    }, function(error){
      alertify.error("Tiliä ei voitu lisätä! ("+error.data.error+")");
    });
  };

  $scope.removeAccount = function remove_account (account) {
    account.remove().then(function(){
      $scope.accounts = _.without($scope.accounts, account);
      alertify.success("Tili poistettu!");
    }, function(){
      alertify.error("Tiliä ei voitu poistaa!");
    });
  };
  $scope.sides = [
    {value: "Vastaava", text: "Vastaava"},
    {value: "Vastattava", text: "Vastattava"}
  ];
  $scope.updateAccount = function update_account (account) {
    account.aid = parseInt(account.aid);
    account.save().then(function () {
      alertify.success("Tili tallennettu!");
    }, function () {
      alertify.error("Tilin tallentaminen epäonnistui");
    });
    return true;
  };
});

lopputiliApp.controller('InvoicesCtrl', function ($scope, Restangular) {
  $scope.invoice_edit_show = false;
  $scope.contacts_by_pk = [];
  Restangular.all('contacts').getList().then(function (contacts) {
    $scope.contacts = contacts;
    contacts.forEach(function (contact) {
      $scope.contacts_by_pk[contact.pk] = contact;
    });
  });
  
  $scope.selectInvoice = function (invoice) {
    $scope.invoice = invoice;
    $scope.invoice_edit_show = true;
  };

   $scope.removeInvoice = function remove_invoice (invoice) {
    invoice.remove().then(function(){
      $scope.invoices = _.without($scope.invoices, invoice);
      alertify.success("Lasku poistettu!");
    }, function(){
      alertify.error("Laskua ei voitu poistaa!");
    });
  };

  Restangular.all('invoices').getList().then(function (invoices) {
    $scope.invoices = invoices;
  });
  $scope.invoice = {
    created: new Date(),
    payment_type: "14 vrk netto",
    due_date: new Date(new Date().getTime() + 14*24*60*60*1000),
    reclamation_time: 7,
    penalty_interest: 7.5,
    summ: 100.0,
    status: "Odottaa"
  };
  $scope.saveInvoice = function (invoice) {
    invoice.invoice_id = parseInt(invoice.invoice_id);
    invoice.penalty_interest = parseFloat(invoice.penalty_interest);
    invoice.reclamation_time = parseInt(invoice.reclamation_time);
    invoice.contact = parseInt(invoice.contact);
    Restangular.all('invoices').post(invoice).then(function (invoice) {
      $scope.invoices.unshift(invoice);
      alertify.success("Lasku tallennettu!");
    }, function () {
      alertify.error("Laskun tallentaminen epäonnistui");
    });
  };
  $scope.toggleInvoiceEdit = function () {
    $scope.invoice_edit_show = !$scope.invoice_edit_show;
  };
});
