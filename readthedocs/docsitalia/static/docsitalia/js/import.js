require=(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
/* Public task tracking */

var jquery = require('jquery');

function poll_task(data) {
    var defer = jquery.Deferred();
    var tries = 5;

    function poll_task_loop() {
        jquery
            .getJSON(data.url)
            .done(function (task) {
                if (task.finished) {
                    if (task.success) {
                        defer.resolve();
                    }
                    else {
                        defer.reject({message: task.error});
                    }
                }
                else {
                    setTimeout(poll_task_loop, 2000);
                }
            })
            .fail(function (error) {
                console.error('Error polling task:', error);
                tries -= 1;
                if (tries > 0) {
                    setTimeout(poll_task_loop, 2000);
                }
                else {
                    var error_msg = error.responseJSON.detail || error.statusText;
                    defer.reject({message: error_msg});
                }
            });
    }

    setTimeout(poll_task_loop, 2000);

    return defer;
}

function trigger_task(config) {
    var defer = jquery.Deferred();
    var url = config.url;
    var token = config.token;
    var data = {csrfmiddlewaretoken: token};

    $.ajax({
        method: 'POST',
        url: url,
        data: data,
        success: function (data) {
            poll_task(data)
                .then(function () {
                    defer.resolve();
                })
                .fail(function (error) {
                    // The poll_task function defer will only reject with
                    // normalized error objects
                    defer.reject(error);
                });
        },
        error: function (error) {
            var error_msg = error.responseJSON.detail || error.statusText;
            defer.reject({message: error_msg});
        }
    });

    return defer;
}

module.exports = {
    poll_task: poll_task,
    trigger_task: trigger_task
};

},{"jquery":"jquery"}],"docsitalia/import":[function(require,module,exports){
var ko = require('knockout');
var tasks = require('readthedocs/core/static-src/core/js/tasks');

$(function () {
  var input = $('#id_repo');
  var repo = $('#id_repo_type');

  input.blur(function () {
    var val = input.val();
    var type;

    switch(true) {
      case /^hg/.test(val):
        type = 'hg';
      break;

      case /^bzr/.test(val):
      case /launchpad/.test(val):
        type = 'bzr';
      break;

      case /trunk/.test(val):
      case /^svn/.test(val):
        type = 'svn';
      break;

      default:
      case /github/.test(val):
      case /(^git|\.git$)/.test(val):
        type = 'git';
      break;
    }

    repo.val(type);
  });
});

function append_url_params(url, params) {
    var link = $('<a>').attr('href', url).get(0);

    Object.keys(params).map(function (key) {
        if (link.search) {
            link.search += '&';
        }
        link.search += key + '=' + params[key];
    });
    return link.href;
}

function Organization(instance, view) {
    var self = this;
    self.id = ko.observable(instance.id);
    self.name = ko.observable(instance.name);
    self.slug = ko.observable(instance.slug);
    self.active = ko.observable(instance.active);
    self.avatar_url = ko.observable(
        append_url_params(instance.avatar_url, {size: 32})
    );
    self.display_name = ko.computed(function () {
        return self.name() || self.slug();
    });
    self.filter_id = ko.computed(function () {
        return self.id();
    });
    self.filter_type = 'org';
    self.filtered = ko.computed(function () {
        var filter = view.filter_by();
        return (
            (filter.id && filter.id !== self.filter_id()) ||
            (filter.type && filter.type !== self.filter_type)
        );
    });
}

function Account(instance, view) {
    var self = this;
    self.id = ko.observable(instance.id);
    self.username = ko.observable(instance.username);
    self.active = ko.observable(instance.active);
    self.avatar_url = ko.observable(
        append_url_params(instance.avatar_url, {size: 32})
    );
    self.provider = ko.observable(instance.provider);
    self.display_name = ko.computed(function () {
        return self.username();
    });
    self.filter_id = ko.computed(function () {
        return self.provider().id;
    });
    self.filter_type = 'own';
    self.filtered = ko.computed(function () {
        var filter = view.filter_by();
        return (
            (filter.id && filter.id !== self.filter_id()) ||
            (filter.type && filter.type !== self.filter_type)
        );
    });
}

function Project(instance, view) {
    var self = this;
    self.id = ko.observable(instance.id);
    self.name = ko.observable(instance.name);
    self.full_name = ko.observable(instance.full_name);
    self.description = ko.observable(instance.description);
    self.vcs = ko.observable(instance.vcs);
    self.organization = ko.observable(instance.organization);
    self.html_url = ko.observable(instance.html_url);
    self.clone_url = ko.observable(instance.clone_url);
    self.ssh_url = ko.observable(instance.ssh_url);
    self.matches = ko.observable(instance.matches);
    self.match = ko.computed(function () {
        var matches = self.matches();
        if (matches && matches.length > 0) {
            return matches[0];
        }
    });
    self.private = ko.observable(instance.private);
    self.active = ko.observable(instance.active);
    self.admin = ko.observable(instance.admin);
    self.is_locked = ko.computed(function () {
        return (self.private() && !self.admin());
    });
    self.avatar_url = ko.observable(
        append_url_params(instance.avatar_url, {size: 32})
    );

    self.import_repo = function () {
        var data = {
                name: self.name(),
                repo: self.clone_url(),
                repo_type: self.vcs(),
                description: self.description(),
                project_url: self.html_url(),
                remote_repository: self.id(),
            };
        var form = $('<form />');

        form
            .attr('action', view.urls.projects_import)
            .attr('method', 'POST')
            .hide();

        Object.keys(data).map(function (attr) {
            var field = $('<input>')
                .attr('type', 'hidden')
                .attr('name', attr)
                .attr('value', data[attr]);
            form.append(field);
        });

        var csrf_field = $('<input>')
            .attr('type', 'hidden')
            .attr('name', 'csrfmiddlewaretoken')
            .attr('value', view.csrf_token);
        form.append(csrf_field);

        // Add a button and add the form to body to satisfy Firefox
        var button = $('<input>')
            .attr('type', 'submit');
        form.append(button);
        $('body').append(form);

        form.submit();
    };
}

function ProjectImportView(instance, config) {
    var self = this;
    var instance = instance || {};

    self.config = config || {};
    self.urls = config.urls || {};
    self.csrf_token = config.csrf_token || '';

    // For task display
    self.error = ko.observable(null);
    self.is_syncing = ko.observable(false);
    self.is_ready = ko.observable(false);

    // For filtering
    self.page_current = ko.observable(null);
    self.page_next = ko.observable(null);
    self.page_previous = ko.observable(null);
    // organization slug or account provider name
    // { id: 'GitHub', type: 'own' }
    self.filter_by = ko.observable({ id: null, type: null });

    self.accounts_raw = ko.observableArray();
    self.organizations_raw = ko.observableArray();
    self.filters = ko.computed(function () {
        var filters = [];
        var accounts_raw = self.accounts_raw();
        var organizations_raw = self.organizations_raw();
        var n;
        for (n in accounts_raw) {
            var account = new Account(accounts_raw[n], self);
            filters.push(account);
        }
        for (n in organizations_raw) {
            var organization = new Organization(organizations_raw[n], self);
            filters.push(organization);
        }
        return filters;
    });
    self.projects = ko.observableArray();

    ko.computed(function () {
        var filter = self.filter_by();
        var url = self.page_current() || self.urls['remoterepository-list'];

        if (!self.page_current()) {
            if (filter.type === 'org') {
                url = append_url_params(
                    self.urls['remoterepository-list'],
                    {org: filter.id}
                );
            }

            if (filter.type === 'own') {
                url = append_url_params(
                    self.urls['remoterepository-list'],
                    {own: filter.id}
                );
            }
        }

        self.error(null);

        $.ajax(url, {
            dataType: "json",
            success: function (projects_list) {
                var projects = [];
                self.page_next(projects_list.next);
                self.page_previous(projects_list.previous);
                var n;
                for (n in projects_list.results) {
                    var project = new Project(projects_list.results[n], self);
                    projects.push(project);
                }
                self.projects(projects);
            },
            error: function (error) {
                var error_msg = error.responseJSON.detail || error.statusText;
                self.error({message: error_msg});
            },
            always: function () {
                self.is_ready(true);
            }
        });
    }).extend({ deferred: true });

    self.get_organizations = function () {
        $.ajax(self.urls['remoteorganization-list'], {
            dataType: "json",
            success: function (organizations) {
                self.organizations_raw(organizations.results);
            },
            error: function (error) {
                var error_msg = error.responseJSON.detail || error.statusText;
                self.error({message: error_msg});
            }
        });
    };

    self.get_accounts = function () {
        $.ajax(self.urls['remoteaccount-list'], {
            dataType: "json",
            success: function (accounts) {
                self.accounts_raw(accounts.results);
            },
            error: function (error) {
                var error_msg = error.responseJSON.detail || error.statusText;
                self.error({message: error_msg});
            }
        });
    };

    self.sync_projects = function () {
        var url = self.urls.api_sync_remote_repositories;

        self.error(null);
        self.is_syncing(true);

        tasks.trigger_task({url: url, token: self.csrf_token})
            .then(function (data) {
                self.get_organizations();
                self.get_accounts();
            })
            .fail(function (error) {
                self.error(error);
            })
            .always(function () {
                self.is_syncing(false);
            });
    };

    self.has_projects = ko.computed(function () {
        return self.projects().length > 0;
    });

    self.next_page = function () {
        self.page_current(self.page_next());
    };

    self.previous_page = function () {
        self.page_current(self.page_previous());
    };

    self.set_filter_by = function (id, type) {
        var filter = self.filter_by();
        if (filter.id === id) {
            filter.id = null;
            filter.type = null;
        }
        else {
            filter.id = id;
            filter.type = type;
        }

        // This needs to use deferred updates because we are setting
        // `filter_by` and `page_current`
        self.filter_by(filter);
        if (filter.id) {
            self.page_current(null);
        }
    };
}


ProjectImportView.init = function (domobj, instance, config) {
    var view = new ProjectImportView(instance, config);
    view.get_accounts();
    view.get_organizations();
    ko.applyBindings(view, domobj);
    return view;
};

module.exports.ProjectImportView = ProjectImportView;

},{"knockout":"knockout","readthedocs/core/static-src/core/js/tasks":1}]},{},[]);
