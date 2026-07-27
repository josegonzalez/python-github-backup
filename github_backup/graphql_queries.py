"""GraphQL query templates used by github-backup."""

DISCUSSION_PAGE_SIZE = 100

CROSS_REFERENCE_PAGE_SIZE = 100

# Cross-references do not change an issue's updatedAt, so the REST listing
# cannot report them as changed. Count and newest timestamp are compared
# against what is on disk: the count alone would miss an add paired with a
# delete, the timestamp alone would miss a delete.
ISSUE_CROSS_REFERENCE_COUNT_QUERY = """
query($owner: String!, $name: String!, $after: String, $pageSize: Int!) {
  repository(owner: $owner, name: $name) {
    issues(first: $pageSize, after: $after) {
      nodes {
        number
        timelineItems(last: 1, itemTypes: [CROSS_REFERENCED_EVENT]) {
          totalCount
          nodes {
            ... on CrossReferencedEvent {
              createdAt
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

# Pull requests are stored as issues when --pulls is not used, and the issues
# connection above excludes them. This query is shaped differently because
# totalCount ignores itemTypes on a pull request, unlike on an issue, so the
# cross-references have to be counted from the nodes themselves.
CROSS_REFERENCE_NODE_LIMIT = 100

PULL_CROSS_REFERENCE_COUNT_QUERY = """
query($owner: String!, $name: String!, $after: String, $pageSize: Int!,
      $nodeLimit: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequests(first: $pageSize, after: $after) {
      nodes {
        number
        timelineItems(last: $nodeLimit, itemTypes: [CROSS_REFERENCED_EVENT]) {
          nodes {
            ... on CrossReferencedEvent {
              createdAt
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

DISCUSSION_LIST_QUERY = """
query($owner: String!, $name: String!, $after: String, $pageSize: Int!) {
  repository(owner: $owner, name: $name) {
    hasDiscussionsEnabled
    discussions(
      first: $pageSize,
      after: $after,
      orderBy: {field: UPDATED_AT, direction: DESC}
    ) {
      totalCount
      nodes {
        id
        number
        title
        updatedAt
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

DISCUSSION_DETAIL_QUERY = """
query(
  $owner: String!,
  $name: String!,
  $number: Int!,
  $commentsCursor: String,
  $pageSize: Int!
) {
  repository(owner: $owner, name: $name) {
    discussion(number: $number) {
      activeLockReason
      answer {
        id
        databaseId
        url
      }
      answerChosenAt
      answerChosenBy {
        ...ActorFields
      }
      author {
        ...ActorFields
      }
      authorAssociation
      body
      bodyHTML
      bodyText
      category {
        createdAt
        description
        emoji
        emojiHTML
        id
        isAnswerable
        name
        slug
        updatedAt
      }
      closed
      closedAt
      createdAt
      createdViaEmail
      databaseId
      editor {
        ...ActorFields
      }
      id
      includesCreatedEdit
      isAnswered
      labels(first: 100) {
        totalCount
        nodes {
          id
          name
          color
          description
        }
      }
      lastEditedAt
      locked
      number
      poll {
        id
        question
        totalVoteCount
        options(first: 100) {
          totalCount
          nodes {
            id
            option
            totalVoteCount
          }
        }
      }
      publishedAt
      reactionGroups {
        ...ReactionGroupFields
      }
      resourcePath
      stateReason
      title
      updatedAt
      upvoteCount
      url
      comments(first: $pageSize, after: $commentsCursor) {
        totalCount
        nodes {
          ...DiscussionCommentFields
          replies(first: $pageSize) {
            totalCount
            nodes {
              ...DiscussionReplyFields
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}

fragment ActorFields on Actor {
  avatarUrl
  login
  resourcePath
  url
}

fragment ReactionGroupFields on ReactionGroup {
  content
  reactors {
    totalCount
  }
}

fragment DiscussionCommentFields on DiscussionComment {
  author {
    ...ActorFields
  }
  authorAssociation
  body
  bodyHTML
  bodyText
  createdAt
  createdViaEmail
  databaseId
  deletedAt
  editor {
    ...ActorFields
  }
  id
  includesCreatedEdit
  isAnswer
  isMinimized
  lastEditedAt
  minimizedReason
  publishedAt
  reactionGroups {
    ...ReactionGroupFields
  }
  replyTo {
    id
    databaseId
    url
  }
  resourcePath
  updatedAt
  upvoteCount
  url
}

fragment DiscussionReplyFields on DiscussionComment {
  author {
    ...ActorFields
  }
  authorAssociation
  body
  bodyHTML
  bodyText
  createdAt
  createdViaEmail
  databaseId
  deletedAt
  editor {
    ...ActorFields
  }
  id
  includesCreatedEdit
  isAnswer
  isMinimized
  lastEditedAt
  minimizedReason
  publishedAt
  reactionGroups {
    ...ReactionGroupFields
  }
  replyTo {
    id
    databaseId
    url
  }
  resourcePath
  updatedAt
  upvoteCount
  url
}
"""

DISCUSSION_REPLIES_QUERY = """
query($commentId: ID!, $repliesCursor: String, $pageSize: Int!) {
  node(id: $commentId) {
    ... on DiscussionComment {
      replies(first: $pageSize, after: $repliesCursor) {
        totalCount
        nodes {
          ...DiscussionReplyFields
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}

fragment ActorFields on Actor {
  avatarUrl
  login
  resourcePath
  url
}

fragment ReactionGroupFields on ReactionGroup {
  content
  reactors {
    totalCount
  }
}

fragment DiscussionReplyFields on DiscussionComment {
  author {
    ...ActorFields
  }
  authorAssociation
  body
  bodyHTML
  bodyText
  createdAt
  createdViaEmail
  databaseId
  deletedAt
  editor {
    ...ActorFields
  }
  id
  includesCreatedEdit
  isAnswer
  isMinimized
  lastEditedAt
  minimizedReason
  publishedAt
  reactionGroups {
    ...ReactionGroupFields
  }
  replyTo {
    id
    databaseId
    url
  }
  resourcePath
  updatedAt
  upvoteCount
  url
}
"""
