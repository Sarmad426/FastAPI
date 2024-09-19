# Quiz App questions

Some questions for the quiz app. It is a `Sqlite` query.

```sql
DELETE FROM quiz;

INSERT INTO quiz (question, options, correct_option) VALUES
('What does HTML stand for?', '["Home Tool Markup Language", "Hyper Text Markup Language", "Hyperlinks and Text Markup Language", "Hyperlinking Text Markup Language"]', 1),
('Which HTML attribute is used to define inline styles?', '["class", "style", "styles", "font"]', 1),
('Which property is used to change the background color in CSS?', '["color", "background-color", "bgcolor", "background"]', 1),
('Which CSS property controls the text size?', '["text-size", "font-size", "font-style", "text-style"]', 1),
('Which HTML element is used to specify a footer for a document or section?', '["<bottom>", "<section>", "<footer>", "<foot>"]', 2),
('Which HTML element is used to define important text?', '["<b>", "<i>", "<strong>", "<important>"]', 2),
('Which CSS property is used to change the text color of an element?', '["color", "text-color", "font-color", "text-style"]', 0),
('Which HTML attribute specifies an alternate text for an image, if the image cannot be displayed?', '["src", "alt", "title", "longdesc"]', 1),
('Which CSS property is used to change the font of an element?', '["font-style", "font-size", "font-family", "font-weight"]', 2),
('Which HTML element is used to define a navigation link?', '["<navigate>", "<navigation>", "<link>", "<nav>"]', 3),
('Which CSS property is used to create space between the element’s border and inner content?', '["border", "padding", "margin", "spacing"]', 1),
('Which HTML element is used to define a table row?', '["<tr>", "<td>", "<table>", "<row>"]', 0),
('Which CSS property is used to change the left margin of an element?', '["padding-left", "margin-left", "left-margin", "margin"]', 1),
('Which HTML element is used to define a list item?', '["<ul>", "<li>", "<ol>", "<item>"]', 1),
('Which CSS property is used to make the text bold?', '["font-style", "font-weight", "text-weight", "text-style"]', 1),
('Which HTML element is used to define a hyperlink?', '["<a>", "<link>", "<href>", "<url>"]', 0),
('Which CSS property is used to change the text alignment of an element?', '["align", "text-align", "text-align-center", "text-style"]', 1),
('Which HTML element is used to define a header for a document or section?', '["<header>", "<head>", "<section>", "<top>"]', 0),
('Which HTML element is used to define a paragraph?', '["<para>", "<p>", "<paragraph>", "<text>"]', 1),
('Which CSS property is used to set the spacing between lines of text?', '["line-height", "spacing", "text-spacing", "line-spacing"]', 0);

```
