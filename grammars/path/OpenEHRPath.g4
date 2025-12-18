// openEHR path grammar (MVP).
//
// Notes:
// - This grammar is intentionally minimal; it covers the path subset used across
//   this repository (Path parsing + resolution + validation).
// - Predicate content is lexed as a single token to avoid mixing in expression
//   grammar at this stage.
//
// Spec: https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html#_paths

grammar OpenEHRPath;

path
    : SLASH segment (SLASH segment)* EOF
    ;

segment
    : IDENT predicate?
    ;

predicate
    : PREDICATE
    ;

SLASH: '/';

// Keep predicate content opaque for now.
// Disallow '/' inside the predicate to avoid accidental path splitting.
PREDICATE: '[' ~[/\u005C\u005B\u005D\r\n]+ ']';

IDENT: [A-Za-z_] [A-Za-z_0-9]*;

WS: [ \t\r\n]+ -> skip;
