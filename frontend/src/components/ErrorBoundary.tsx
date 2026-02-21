import { Component, type ErrorInfo, type ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    errorMessage: string;
}

class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false, errorMessage: '' };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, errorMessage: error.message };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
        console.error('[ErrorBoundary] caught:', error, errorInfo);
    }

    handleReset = (): void => {
        this.setState({ hasError: false, errorMessage: '' });
    };

    render(): ReactNode {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-8">
                    <div className="bg-white rounded-xl shadow-lg border border-danger-700/20 p-10 max-w-md text-center space-y-4">
                        <div className="mx-auto w-16 h-16 bg-danger-700/10 rounded-full flex items-center justify-center">
                            <AlertTriangle className="w-8 h-8 text-danger-700" />
                        </div>
                        <h2 className="text-xl font-bold text-primary-900">Something went wrong</h2>
                        <p className="text-sm text-neutral-400">
                            {this.state.errorMessage || 'An unexpected error occurred. Please try again.'}
                        </p>
                        <button
                            onClick={this.handleReset}
                            className="mt-4 px-6 py-2 bg-secondary-500 text-white rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                        >
                            Try Again
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
