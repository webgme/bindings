/* eslint-env mocha, node */

describe('BindingsDocs', function() {
    var testFixture = require('../../globals'),
        superagent = testFixture.superagent,
        expect = testFixture.expect,
        gmeConfig = testFixture.getGmeConfig(),
        server = testFixture.WebGME.standaloneServer(gmeConfig),
        mntPt = require('../../../webgme-setup.json').components.routers['BindingsDocs'].mount,
        urlFor = function(action) {
            return [
                server.getUrl(),
                mntPt,
                action
            ].join('/');
        };

    before(function(done) {
        server.start(done);
    });

    after(function(done) {
        server.stop(done);
    });

    it('should get description about languages', function(done) {
        superagent.get(urlFor(''))
            .end(function(err, res) {
                try {
                    expect(res.statusCode).to.equal(200);
                    expect(res.body.python).to.equal(urlFor('python/index.html'));
                    done();
                } catch (e) {
                    done(e);
                }
            });
    });

    it('should serve python/index.html at index.html', function(done) {
        superagent.get(urlFor('python/index.html'))
            .end(function(err, res) {
                try {
                    expect(res.statusCode).to.equal(200);
                    expect(res.text).to.include('<body>');
                    done();
                } catch (e) {
                    done(e);
                }
            });
    });

    it('should serve python/index.html at /', function(done) {
        superagent.get(urlFor('python/'))
            .end(function(err, res) {
                try {
                    expect(res.statusCode).to.equal(200);
                    expect(res.text).to.include('<body>');
                    done();
                } catch (e) {
                    done(e);
                }
            });
    });
});
