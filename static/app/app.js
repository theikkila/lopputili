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
    controller: 'DashboardCtrl',
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
  //RestangularProvider.setParentless(true);
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


lopputiliApp.controller('DashboardCtrl', function ($scope, Restangular) {
  Restangular.all('invoices').getList().then(function (invoices) {
    $scope.invoices = invoices;
    $scope.paid = invoices.filter(function (invoice) {
      return invoice.status == "Maksettu";
    });
  });
  Restangular.all('contacts').getList().then(function (contacts) {
    $scope.contacts = contacts;
  });
});

lopputiliApp.controller('ReceiptsCtrl', function ($scope, Restangular) {
  $scope.accounts_by_pk = [];
  $scope.commits = [];
  Restangular.all('accounts').getList().then(function (accounts) {
    $scope.accounts = accounts;
    accounts.forEach(function(account){
      $scope.accounts_by_pk[account.pk] = account;
    });
  });
  $scope.totals = function () {
    return $scope.commits.reduce(function(cumulative, current) {
      cumulative.debet += current.debet_amount;
      cumulative.credit += current.credit_amount;
      return cumulative;
    }, {debet:0, credit:0});
  }
  $scope.saveCommit = function (commit) {
    commit.debet_amount = parseFloat(commit.debet_amount);
    commit.credit_amount = parseFloat(commit.credit_amount);
    var account = commit.account;
    commit.account = commit.account.pk
    commit.parentResource = null;
    commit.save().then(function () {
      commit.account = account;
      alertify.success("Tapahtuma tallennettu!");
    });
  }
  $scope.removeCommit = function (commit) {
    commit.remove().then(function () {
      alertify.success("Tapahtuma poistettu!");
      $scope.commits = _.without($scope.commits, commit);
    });
  };
  $scope.removeReceipt = function (receipt) {
    receipt.remove().then(function () {
      alertify.success("Tosite poistettu!");
      $scope.receipts = _.without($scope.receipts, receipt);
    });
  };
  $scope.addCommit = function add_commit () {
    var c = {receipt: $scope.selected.pk, credit_amount:0, debet_amount:0, account: 1};
    Restangular.all('commits').post(c).then(function (commit) {
      $scope.commits.push(commit);
      alertify.success("Tapahtuma lisätty!");
    });
  };
  $scope.addReceipt = function add_receipt () {
    var r = {rid:$scope.receipts.length+1, commit_date: new Date()};
    Restangular.all('receipts').post(r)
    .then(function (receipt) {
      $scope.receipts.unshift(receipt);
    });
  };
  $scope.updateReceipt = function update_receipt (receipt) {
      receipt.save().then(function (receipt) {
        alertify.success("Tosite tallennettu!");
      });
  };
  Restangular.all('receipts').getList().then(function (receipts) {
    $scope.receipts = receipts.map(function (receipt) {
      receipt.commit_date = new Date(receipt.commit_date);
      return receipt;
    });
  });
  $scope.editReceipt = function edit_receipt (receipt) {
    $scope.selected = receipt;
    receipt.all('commits').getList().then(function (commits) {
      $scope.commits = commits.map(function (commit) {
        var p = commit.account;
        //console.log(p);
        commit.account = _.find($scope.accounts, {pk:p});
        //console.log(commit);
        return commit;
      });
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
  $scope.invoices = [];
  $scope.contacts_by_pk = [];
  Restangular.all('contacts').getList().then(function (contacts) {
    $scope.contacts = contacts;
    contacts.forEach(function (contact) {
      $scope.contacts_by_pk[contact.pk] = contact;
    });
  });
  
  $scope.selectInvoice = function (invoice) {
    $scope.invoice = invoice;
    $scope.invoice.created = new Date(invoice.created);
    $scope.invoice.due_date = new Date(invoice.due_date);
    $scope.invoice.products = [];
    invoice.all('products').getList().then(function (products) {
      $scope.invoice.products = products;
    });
    $scope.invoice_edit_show = true;
  };

   $scope.removeInvoice = function (invoice) {
    invoice.remove().then(function(){
      $scope.invoices = _.without($scope.invoices, invoice);
      alertify.success("Lasku poistettu!");
    }, function(){
      alertify.error("Laskua ei voitu poistaa!");
    });
  };

  $scope.paidInvoice = function (invoice) {
    invoice.status = "Maksettu";
    invoice.save().then(function (invoice) {
      alertify.success("Lasku "+invoice.title+" merkitty maksetuksi.");
    }, function () {
      alertify.error("Laskua ei voitu merkitä maksetuksi!");
    });
  }

  Restangular.all('invoices').getList().then(function (invoices) {
    $scope.invoices = invoices;
    $scope.invoice.invoice_id = invoices.length+1;
  });
  $scope.invoice = blankInvoice();
  $scope.saveInvoice = function (invoice) {
    invoice.invoice_id = parseInt(invoice.invoice_id);
    invoice.penalty_interest = parseFloat(invoice.penalty_interest);
    invoice.reclamation_time = parseInt(invoice.reclamation_time);
    invoice.contact = parseInt(invoice.contact);
    invoice.products = invoice.products.map(function (product) {
      product.price = parseFloat(product.price);
      return product;
    });
    //delete invoice.products;
    var iv = Restangular.restangularizeElement(null, invoice, 'invoices');
    iv.fromServer = (iv.pk != undefined);
    iv.save().then(function (invoice) {
      $scope.invoice.products.forEach(function (product) {
        product.invoice = invoice.pk;
        var p = Restangular.restangularizeElement(null, product, 'products');
        p.fromServer = (p.pk != undefined);
        p.save().then(function (product) {
          alertify.success("Tuote "+product.name+" tallennettu!");
        });
      });
      if(!iv.fromServer){
        $scope.invoices.unshift(invoice);
      }
      $scope.invoice = blankInvoice();
      alertify.success("Lasku tallennettu!");

    }, function () {
      alertify.error("Laskun tallentaminen epäonnistui");
    });
  };
  $scope.toggleInvoiceEdit = function () {
    $scope.invoice_edit_show = !$scope.invoice_edit_show;
  };
  $scope.addProduct = function () {
    $scope.invoice.products.push(blankProduct($scope.invoice.pk));
  };
  $scope.removeProduct = function (product) {
    if(product.pk) {
      Restangular.one('products', product.pk).remove().then(function () {
        $scope.invoice.products = _.without($scope.invoice.products, product);
        alertify.success("Tuoterivi poistettu!");
      });
    } else {
        $scope.invoice.products = _.without($scope.invoice.products, product);
        alertify.success("Tuoterivi poistettu!");
    }
  }
  function blankProduct (invid) {
    return {
      invoice: invid,
      name: "Tuote",
      price: 0,
      count: 1,
      discount: 0,
      vat: 24
    };
  }
  $scope.totals = function () {
    return $scope.invoice.products.map(function (product) {
      var discount = product.discount/100;
      var line_brutto = product.price*product.count;
      var discount_value = line_brutto*discount;
      var line_after_discount = line_brutto-discount_value;
      var vat_percent = product.vat / 100;
      var taxes = line_after_discount * vat_percent;
      var total = line_after_discount + taxes;
      return {taxes: taxes, brutto_total: total, netto_total: line_after_discount};
    }).reduce(function(cumulative, line){
      cumulative.taxes += line.taxes;
      cumulative.brutto_total += line.brutto_total;
      cumulative.netto_total += line.netto_total;
      return cumulative;
    }, {taxes: 0, brutto_total: 0, netto_total: 0});
  }
  function blankInvoice(){
    return {
      invoice_id: $scope.invoices.length+1,
      created: new Date(),
      payment_type: "14 vrk netto",
      due_date: new Date(new Date().getTime() + 14*24*60*60*1000),
      reclamation_time: 7,
      penalty_interest: 7.5,
      status: "Odottaa",
      products: []
    }
  }
});
