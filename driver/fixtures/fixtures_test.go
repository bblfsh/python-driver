package fixtures

import (
	"path/filepath"
	"testing"

	"github.com/bblfsh/python-driver/driver/normalizer"
	"gopkg.in/bblfsh/sdk.v2/sdk/driver"
	"gopkg.in/bblfsh/sdk.v2/sdk/driver/fixtures"
	"os"
)

const projectRoot = "../../"

var Suite = &fixtures.Suite{
	Lang: "python",
	Ext:  ".py",
	Path: filepath.Join(projectRoot, fixtures.Dir),
	NewDriver: func() driver.BaseDriver {
		return driver.NewExecDriverAt(filepath.Join(projectRoot,
			"build/.local/bin/python_driver"))
	},
	Transforms: normalizer.Transforms,
	BenchName:  "issue_server101",
	//Docker:fixtures.DockerConfig{
		//Image:"python:3",
	//},
	Semantic: fixtures.SemanticConfig{
		BlacklistTypes: []string{
			"AsyncFunctionDef",
			"Bytes",
			"FunctionDef",
			"Import",
			"ImportFrom",
			"Name",
			"NoopLine",
			"NoopSameLine",
			"QualifiedIdentifier",
			"Str",
			"StringLiteral",
			"arg",
			"kwarg",
			"kwonly_arg",
			"vararg",
		},
	},
}

func SetPythonPath() {
	os.Setenv("PYTHONPATH", filepath.Join(projectRoot,
		"build/.local/lib/python3.6/site-packages"))
}

func TestPythonDriver(t *testing.T) {
	SetPythonPath()
	Suite.RunTests(t)
}

func BenchmarkPythonDriver(b *testing.B) {
	SetPythonPath()
	Suite.RunBenchmarks(b)
}
