import React from 'react';

export function decodeEntities(value = '') {
  return value
    .replace(/&#x20;|&#32;/gi, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'");
}

export function parseInlineText(str = '') {
  const source = decodeEntities(str);
  const parts = [];

  const regex =
    /(\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)|\*\*.*?\*\*|https?:\/\/[^\s)]+|`.*?`)/g;

  let lastIndex = 0;
  let match;

  while ((match = regex.exec(source)) !== null) {
    if (match.index > lastIndex) {
      parts.push(
        source.substring(lastIndex, match.index)
      );
    }

    const token = match[0];

    if (token.startsWith('[')) {
      const link = token.match(
        /^\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)$/
      );

      if (link) {
        parts.push(
          <a
            key={match.index}
            href={link[2]}
            target="_blank"
            rel="noopener noreferrer"
            className="doc-link"
          >
            {link[1]}
          </a>
        );
      }
    } else if (
      token.startsWith('**') &&
      token.endsWith('**')
    ) {
      parts.push(
        <strong key={match.index}>
          {token.slice(2, -2)}
        </strong>
      );
    } else if (
      token.startsWith('`') &&
      token.endsWith('`')
    ) {
      parts.push(
        <code
          key={match.index}
          className="doc-code"
        >
          {token.slice(1, -1)}
        </code>
      );
    } else {
      parts.push(
        <a
          key={match.index}
          href={token}
          target="_blank"
          rel="noopener noreferrer"
          className="doc-link"
        >
          {token}
        </a>
      );
    }

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < source.length) {
    parts.push(source.substring(lastIndex));
  }

  return parts.length ? parts : source;
}