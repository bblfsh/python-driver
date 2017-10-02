package normalizer

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
	"gopkg.in/bblfsh/sdk.v1/uast"
)

var (
	fixtureDir = "fixtures"
)

func TestAnnotate(t *testing.T) {
	require := require.New(t)

	f, err := getFixture("python_example_1.json")
	require.NoError(err)

	n, err := ToNode.ToNode(f)
	require.NoError(err)
	require.NotNil(n)

	err = AnnotationRules.Apply(n)
	require.NoError(err)

	missingRole := make(map[string]bool)
	iter := uast.NewOrderPathIter(uast.NewPath(n))
	for {
		n := iter.Next()
		if n.IsEmpty() {
			break
		}

		missingRole[n.Node().InternalType] = true
	}
}

func TestAnnotatePrettyAnnotationsOnly(t *testing.T) {
	require := require.New(t)

	f, err := getFixture("python_example_1.json")
	require.NoError(err)

	n, err := ToNode.ToNode(f)
	require.NoError(err)
	require.NotNil(n)

	err = AnnotationRules.Apply(n)
	require.NoError(err)
}

func TestNodeTokens(t *testing.T) {
	require := require.New(t)

	f, err := getFixture("python_example_1.json")
	require.NoError(err)

	n, err := ToNode.ToNode(f)
	require.NoError(err)
	require.NotNil(n)

	tokens := uast.Tokens(n)
	require.True(len(tokens) > 0)
	//func Pretty(n *Node, w io.Writer, includes IncludeFlag) error {
	err = uast.Pretty(n, os.Stdout, uast.IncludeAll)
	require.NoError(err)
}

func TestAll(t *testing.T) {
	require := require.New(t)

	f, err := getFixture("python_example_1.json")
	require.NoError(err)

	n, err := ToNode.ToNode(f)
	require.NoError(err)
	require.NotNil(n)

	tokens := uast.Tokens(n)
	require.True(len(tokens) > 0)

	err = AnnotationRules.Apply(n)
	require.NoError(err)

	//func Pretty(n *Node, w io.Writer, includes IncludeFlag) error {
	err = uast.Pretty(n, os.Stdout, uast.IncludeAll)
	require.NoError(err)
}

func getFixture(name string) (map[string]interface{}, error) {
	path := filepath.Join(fixtureDir, name)
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	d := json.NewDecoder(f)
	data := map[string]interface{}{}
	if err := d.Decode(&data); err != nil {
		_ = f.Close()
		return nil, err
	}

	if err := f.Close(); err != nil {
		return nil, err
	}

	return data, nil
}
