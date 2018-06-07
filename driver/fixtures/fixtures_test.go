package fixtures

import (
	"path/filepath"
	"testing"

	"github.com/bblfsh/python-driver/driver/normalizer"
	"gopkg.in/bblfsh/sdk.v2/sdk/driver"
	"gopkg.in/bblfsh/sdk.v2/sdk/driver/fixtures"
)

const projectRoot = "../../"

var Suite = &fixtures.Suite{
	Lang: "python",
	Ext:  ".py",
	Path: filepath.Join(projectRoot, fixtures.Dir),
	NewDriver: func() driver.BaseDriver {
		return driver.NewExecDriverAt(filepath.Join(projectRoot, "build/bin/native"))
	},
	Transforms: driver.Transforms{
		Preprocess: normalizer.Preprocess,
		Normalize: normalizer.Normalize,
		Native: normalizer.Native,
		Code:   normalizer.Code,
	},
	BenchName: "issue_server101",
	// XXX check this
	//Semantic: fixtures.SemanticConfig{
		//BlacklistTypes: []string{
			//"StringLiteral",
			//"SimpleName",
			//"QualifiedName",
			//"BlockComment",
			//"LineComment",
			//"Block",
			//"ImportDeclaration",
			//"MethodDeclaration",
		//},
	//},
}

func TestPythonDriver(t *testing.T) {
	Suite.RunTests(t)
}

func BenchmarkPythonDriver(b *testing.B) {
	Suite.RunBenchmarks(b)
}
