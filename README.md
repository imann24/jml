# JML
Parses XML from a custom JSON schema with a few added macros

## Usage:
`python convert.py <path to JSON file>`

## Example
`python convert.py test/test_input`

## Schema:
1. `el` - the element type/tag
1. `attr` - the attributes on the element
1. `children` - the child (nested) elements
1. `inner` - the inner text for an element

## Supported Macros:
1. `repeat` - how many times to repeat an XML element
1. `repeat_mods` - what modifications to run on an XML element each time it's repeated
    1. `ADD:<number>` - add an incrementing number to an XML attribute each time it's repeated (_base attribute value must also be a number_)
    1. `APPEND:IDX` - append the repeat index to an XML element attribute
1. `attr_providers` - an array of values for an attribute which map by index
1. `inner_providers` - an array of values for inner text which map by index

## Specs
Developed with `Python 2.7.9`
