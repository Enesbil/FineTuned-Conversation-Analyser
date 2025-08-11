# Contributing to Fine-Tuned Sentiment Analyzer

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Fine-Tuned Sentiment Analyzer.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/fine-tuned-sentiment-analyser.git
   cd fine-tuned-sentiment-analyser
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your environment** by copying `secrets.env.example` to `secrets.env` and adding your OpenAI API key

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small when possible

### Commit Messages

Use clear and descriptive commit messages:
- `feat: add new analysis category for catering services`
- `fix: handle empty conversation transcripts properly`
- `docs: update README with new installation steps`
- `refactor: improve conversation preprocessing logic`

### Testing

Before submitting a pull request:
1. Test your changes with sample data
2. Ensure the conversation analyzer runs without errors
3. Verify the manual labeling interface works correctly
4. Check that JSONL validation still passes

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- Sample data (if possible, anonymized)
- Error messages or logs

### Feature Requests

For new features, please:
- Describe the use case and benefits
- Provide examples of how it would work
- Consider backward compatibility
- Discuss implementation approach

### Code Contributions

#### Areas for Improvement

1. **Analysis Categories**: Add new conversation categories for different domains
2. **Language Support**: Extend beyond Turkish to other languages
3. **Model Integration**: Support for other LLM providers beyond OpenAI
4. **Data Processing**: Improve conversation preprocessing and cleaning
5. **UI/UX**: Enhance the manual labeling interface
6. **Performance**: Optimize for large datasets
7. **Validation**: Add more robust data validation and error handling

#### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly** with various conversation types

4. **Update documentation** if needed (README, docstrings, etc.)

5. **Submit a pull request** with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots for UI changes
   - Examples of new functionality

## Code Organization

### Key Files

- `conversation_analyzer.py`: Main analysis logic and OpenAI integration
- `conversation_labeler.html`: Manual labeling web interface
- `process_conversations.py`: Data preprocessing and cleaning
- `validate_jsonl.py`: Fine-tuning data validation

### Adding New Features

#### New Analysis Categories

To add new conversation categories:

1. Update the categories list in `conversation_analyzer.py` (lines 58-64)
2. Update the categories in `conversation_labeler.html` if needed
3. Update the analysis prompt to include the new categories
4. Test with sample conversations that fit the new categories

#### New Analysis Metrics

To add new analysis dimensions:

1. Update the JSON schema in `conversation_analyzer.py` (lines 32-81)
2. Update the analysis prompt with guidelines for the new metric
3. Update the manual labeling interface to include the new field
4. Update validation logic if needed

#### New Language Support

To add support for new languages:

1. Translate the analysis prompt and categories
2. Update text processing in `process_conversations.py` if needed
3. Consider language-specific preprocessing requirements
4. Update documentation with language-specific examples

## Documentation

### README Updates

When adding features, update the README with:
- New installation or setup steps
- Usage examples for new features
- Configuration options
- API documentation updates

### Code Documentation

- Add docstrings to new functions and classes
- Include parameter types and return value descriptions
- Provide usage examples for complex functions

## Community Guidelines

- Be respectful and constructive in discussions
- Help others learn and improve
- Share knowledge and best practices
- Report issues and bugs responsibly

## Questions?

If you have questions about contributing:
1. Check existing issues and discussions
2. Create a new issue with the "question" label
3. Be specific about what you're trying to achieve

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making conversation analysis better for everyone!
