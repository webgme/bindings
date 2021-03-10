/* eslint-env mocha, node */

describe('PythonBindings', function () {
    var testFixture = require('../../globals'),
        gmeConfig = testFixture.getGmeConfig(),
        expect = testFixture.expect,
        logger = testFixture.logger.fork('PythonBindings'),
        PluginCliManager = testFixture.WebGME.PluginCliManager,
        projectName = 'testProject',
        pluginName = 'PythonBindings',
        project,
        gmeAuth,
        storage,
        commitHash;

    before(function (done) {
        this.timeout(10000);
        testFixture.clearDBAndGetGMEAuth(gmeConfig, projectName)
            .then(function (gmeAuth_) {
                gmeAuth = gmeAuth_;
                // This uses in memory storage. Use testFixture.getMongoStorage to persist test to database.
                storage = testFixture.getMemoryStorage(logger, gmeConfig, gmeAuth);
                return storage.openDatabase();
            })
            .then(function () {
                var importParam = {
                    projectSeed: testFixture.path.join(testFixture.SEED_DIR, 'EmptyProject.webgmex'),
                    projectName: projectName,
                    branchName: 'master',
                    logger: logger,
                    gmeConfig: gmeConfig
                };

                return testFixture.importProject(storage, importParam);
            })
            .then(function (importResult) {
                project = importResult.project;
                commitHash = importResult.commitHash;
                return project.createBranch('test', commitHash);
            })
            .nodeify(done);
    });

    after(function (done) {
        storage.closeDatabase()
            .then(function () {
                return gmeAuth.unload();
            })
            .nodeify(done);
    });

    it('should run plugin and succeed', function (done) {
        var manager = new PluginCliManager(null, logger, gmeConfig),
            pluginConfig = {
            },
            context = {
                project: project,
                commitHash: commitHash,
                branchName: 'test',
                activeNode: '/1',
            };

        manager.executePlugin(pluginName, pluginConfig, context, function (err, pluginResult) {
            try {
                expect(err).to.equal(null);
                expect(typeof pluginResult).to.equal('object');
                expect(pluginResult.success).to.equal(true);
                expect(pluginResult.messages.length).to.equal(1);
                expect(pluginResult.messages[0].message).to.include('Hello');
                expect(pluginResult.artifacts.length).to.equal(1);
                done();
            } catch (e) {
                done(e);
            }
        });
    });
});
