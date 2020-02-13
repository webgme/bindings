/* eslint-env mocha, node */

describe.skip('corezmq-server', function () {
    const testFixture = require('../globals'),
        corezmq_server = require('../../bin/corezmq_server'),
        cp = require('child_process'),
        gmeConfig = testFixture.getGmeConfig(),
        //expect = testFixture.expect,
        logger = testFixture.logger.fork('PythonBindings'),
        projectName = 'PythonTestProject',
        PYTHON_TEST_TOP_DIR = testFixture.path.join(process.cwd(), 'python', 'webgme_bindings'),
        PYTHON_TEST_START_DIR = testFixture.path.join(PYTHON_TEST_TOP_DIR, 'webgme_bindings');

    const callScript = (program, args, env) => {
        let deferred = testFixture.Q.defer();

        const childProc = cp.spawn(program, args, {env});

        childProc.stdout.on('data', data => {
            logger.debug(data.toString());
        });

        childProc.stderr.on('data', data => {
            logger.error(data.toString());
        });

        childProc.on('close', (code) => {
            if (code > 0) {
                deferred.reject(new Error(`${program} ${args.join(' ')} exited with code ${code}.`));
            } else {
                deferred.resolve();
            }
        });

        childProc.on('error', (err) => {
            deferred.resolve(err);
        });

        return deferred.promise;
    };

    let project,
        gmeAuth,
        storage,
        commitHash,
        zmqServer;

    before(function (done) {
        testFixture.clearDBAndGetGMEAuth(gmeConfig)
            .then((gmeAuth_) => {
                gmeAuth = gmeAuth_;
                storage = testFixture.getMongoStorage(logger, gmeConfig, gmeAuth);
                return storage.openDatabase();
            })
            .then(() => {
                const importParam = {
                    projectSeed: testFixture.path.join(testFixture.SEED_DIR, 'EmptyProject.webgmex'),
                    projectName: projectName,
                    branchName: 'master',
                    logger: logger,
                    gmeConfig: gmeConfig
                };

                return testFixture.importProject(storage, importParam);
            })
            .then((importResult) => {
                project = importResult.project;
                return storage.closeDatabase();
            })
            .then(() => {
                return gmeAuth.unload();
            })
            .nodeify(done);
    });

    afterEach(function (done) {
        if (zmqServer) {
            zmqServer.shutdown().finally(done);
        } else {
            done();
        }
    });

    it('should start corezmq server and then run the python tests', function (done) {
        this.timeout(10 * 60 * 1000); // 10 min

        corezmq_server({
            projectName,
            gmeConfig,
            logger,
            port: 5555,
        })
            .then((zmqServer_) => {
                zmqServer = zmqServer_;
                // Tell python tests to not start the corezmq server.
                const pyEnv = {'DO_NOT_START_SERVER': 'notEmpty'};

                Object.keys(process.env)
                    .forEach((key) => {
                        pyEnv[key] = process.env[key];
                    });

                const args = [
                    '-m', 'unittest',
                    'discover',
                    '-s', PYTHON_TEST_START_DIR,
                    '-p', 'test.py', // (pattern)
                    '-t', PYTHON_TEST_TOP_DIR
                ];

                console.log(`python ${args.join(' ')}`);
                return callScript('python', args, pyEnv);
            })
            .nodeify(done);
    });
});